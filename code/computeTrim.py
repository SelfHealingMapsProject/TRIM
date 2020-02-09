import csv

import numpy as np, pandas as pd
from math import exp, log
from scipy.stats import entropy
from scipy.stats import boxcox

from params import *
from utils import genGridIds, neigbourGrids, removeRepetition
from fullTree import countwalksDP


def entOdTree(trips):
    '''
    recieves the list of sequence of trips.
    the number of leaves in the prefix tree is equal to
    the number of unique lists in trips
    '''

    numLeaf = len(set(trips))
    counts  = {x:trips.count(x) for x in set(trips)}
    probs   = [float(c)/len(trips) for c in counts.values()]
    return abs(entropy(probs))


def computeTrim(trips, neigbourDict, distMatrix, counts):
    '''
    recieves the list of sequence of trips, the dictionary to look up each cell's
    neighbours, the distance matrix for all pairs of nodes in the graph and the
    3D matrix with the number of leaves of the full tree for all the origin,
    destination and budgets.
    '''
    origin = trips[0][0]
    dest   = trips[0][-1]
    budget = max([len(t) for t in trips])

    if budget >= len(counts[0][0]):
        return np.NaN, budget, np.NaN, budget

    if budget < distMatrix[int(origin), int(dest)]:
        return np.NaN, budget, np.NaN, budget

    ent = entOdTree (trips)
    if ent == 0.0:
        return 0.0, 0.0, np.NaN, budget
    num     = len(trips)
    ways    = counts[int(origin)][int(dest)][budget]

    if  ways >= num:
        denom = ways

    else:
        # if the number of trips is larger than the number of leaves in the
        # full tree, then we randomly generate a list of 'num' sequences and
        # compute the entropy for that list.
        rand  = np.random.choice(ways, num, replace = True)
        temp  = [trips[i] for i in rand]
        denom = entOdTree (temp)

    return (ent/denom), ent, denom, budget

def postProcess(measures):
    '''normalising trim scores to address the bias introduced by the varying number
    of trips and varying budgets
    '''
    R = pd.DataFrame([[line[0]]+line[-7:] for line in measures],\
    columns = ['uID', 'o', 'd', '#trips', 'budget', 'trim', 'ent', 'ways'])

    R   = R[R['trim'].notnull()]
    eps = R[R['trim'] > 0]['trim'].min()

    minB = R['budget'].min()
    maxB = R['budget'].max()
    temp = ((R['budget'] - minB)/(maxB-minB))-1
    R['weightB'] = temp.apply(exp)

    minT = R['#trips'].min()
    maxT = R['#trips'].max()
    temp = ((R['#trips'] - minT)/(maxT-minT))
    R['weightT'] = temp.apply(exp)

    temp = R['trim'].map(lambda x:boxcox(x+eps,0.0))
    R['normalised Trim'] = temp*R['weightB']*R['weightT']
    return R




if __name__ == "__main__":

    # n determines the size of the grid cells with
    # larger n corresponding to finer grids
    gridList, zDict = genGridIds(n)
    adjDict = neigbourGrids(n, gridList, zDict)

    if ST:
        # if remaining in the same cell is allowed; default is False
        newAdjDict = {x: list(v)+[x] for x, v in adjDict.items()}
        for i in range(delta.shape[0]): delta[i,i] = 1.0
    else:
        newAdjDict = {x: list(v) for x, v in adjDict.items()}

    delta   = np.loadtxt('../data/pairDist-level'+str(n)+'.csv', delimiter = ',')

    odPairs = []
    with open('../data/geoLife-mapped-level'+str(n)+'.txt', 'r') as inFile:
        mappedData = list(csv.reader(inFile))

    if ST:
        tLen   = np.array([len(i)-3 for i in mappedData])
    else:
        tLen   = np.array([len(removeRepetition(i[2:])) for i in mappedData])

    maxBgt = max(int(np.mean(tLen)+3*np.std(tLen)), MAX_B)
    counts = countwalksDP(newAdjDict, maxBgt)

    odData = pd.DataFrame([[i[0],i[1],i[2], i[-1]] for i in mappedData],\
            columns = ['uId', 'tId', 'o', 'd'])
    grouped =  odData.groupby(by = ['uId', 'o', 'd'])
    for g, info in grouped:
        odPairs.append([g[0],info.tId.values.tolist()])

    tripMeasures = []
    for pair in odPairs:
        trips = []
        uID  = pair[0]
        for tID in pair[1]:
            if ST:
                trips+= [i[2:] for i in mappedData\
                if i[0] == uID and i[1]== tID]
            else:
                trips+= [removeRepetition(i[2:]) for i in mappedData\
                if i[0] == uID and i[1]== tID]
        if trips == []: continue
        trim,ent, ways, budget = computeTrim(list(map(tuple,trips)), newAdjDict, delta, counts)
        tripMeasures.append([uID]+pair[1]+[trips[0][0], trips[0][-1], len(trips),budget, trim, ent, ways])

    results = postProcess(tripMeasures)
    results.to_csv('../output/results-level'+str(n)+'.csv', encoding='utf-8', index=False)

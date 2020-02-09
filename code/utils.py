
def decToBin(n):
    # print ('and then here', n, int(decToBin(n/2)) + str(n%2))
    # print ()
    if n==0: return ''
    else:
        return decToBin(n//2) + str(n%2)

def bitShuffling(row, column, level):
    rowBin = decToBin(int(row))
    colBin = decToBin(int(column))
    if len(rowBin) < level:
        rowBin = '0'*(level-len(rowBin))+ rowBin
    if len(colBin) < level:
        colBin = '0'*(level-len(colBin))+ colBin
    bitShuffled = ''
    for i in range(len(rowBin)):
        bitShuffled += rowBin[i]+colBin[i]
    return bitShuffled


def convert2zvalue(row, column, level):
    bitShuffled = bitShuffling(row, column, level)
    return sum(int(c) * (2 ** i) for i, c in enumerate(bitShuffled[::-1]))

def genGridIds(n):
    gridIdList = []
    for i in range(2**n):
        for j in range(2**n):
            gridIdList.append((i,j))
    grid2zID = {x: convert2zvalue(x[0], x[1], n) for x in gridIdList }
    return gridIdList, grid2zID

def neigbourGrids(n, gridIdList, grid2zID):
    maxID  = 2**n - 1
    gridNeigbours = {}
    for id in gridIdList:
        i = id[0]
        j = id[1]
        neigbours = [(i, j-1), (i, j+1),(i-1, j), (i+1,j),\
                    (i-1, j-1), (i+1, j+1),(i-1, j+1), (i+1,j-1)]
        neigbours = [n for n in neigbours if 0<=n[0]<=maxID and 0<=n[1]<=maxID]
        # map to zcurve
        gridNeigbours[str(grid2zID[id])] = set([str(grid2zID[n]) for n in neigbours])
    return gridNeigbours

def removeRepetition(l):
    newList = [l[0]]
    for elem in l[1:]:
        if elem == newList[-1]: continue
        newList.append(elem)
    return newList

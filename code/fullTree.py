def countwalksRecursive(graph, u, v, k):

    # Base cases
    if (k == 0 and u == v):
        return 1
    if (k == 1 and v in graph[u]):
        return 1
    if (k <= 0):
        return 0

    # Initialize result
    count = 0

    # Go to all adjacents of u and recur
    for i in range(0, v):

        # Check if is adjacent of u
        if (v in graph[u]):
            count += countwalksRecursive(graph, i, v, k-1)

    return count


def countwalksDP(graph,k):

    # Table to be filled up using DP. The value count[i][j][e] will
    # store count of possible walks from i to j with exactly k edges
    # s = dt.now()
    V = len(graph)
    nk = k+1

    count = [[[0]*nk for i in range(V)] for i in range(V)]
    for e in range(1,nk):
        for i in range(V):
            for j in range(V):

                # base cases
                if e == 1 and i == j:
                    count[i][j][e] = 1
                if e == 1 and str(j) in graph[str(i)]:
                    # print ('here?', i, j)

                    count[i][j][e] = 1
                # go to adjacent only when number of edges is more than 1
                if e > 1:
                    for a in range(V):
                        if str(a) in graph[str(i)]:
                            # print ('does it get here?')
                            # print (a, j, e-1, count[a,j,e-1])
                            count[i][j][e] += count[a][j][e-1]
                            if count[i][j][e] < 0: print (i,j,e)

    return count

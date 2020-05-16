import numpy as np
import pandas as pd

def find_match(dataCleaned, n):
    flat = [(i[1:4] + list(i[4].values())) for i in dataCleaned]
    flat = pd.get_dummies(pd.DataFrame(flat)) # One hot encoding of categorical variables

    arr = flat.to_numpy()
    arr = (arr - arr.min(axis = 0)) / (arr.max(axis=0) - arr.min(axis=0)) # Feature scaling to 0:1
    weights = [1,1,1,1,1,1] + [2 for i in range(6,len(arr[0]))]
    arr = arr * weights # Higher weightage for certain features

    user = arr[0]
    arr = arr[1:]
    dist = (arr - user)**2 # Calculate Euclidean distance
    dist = np.sum(dist, axis=1)
    dist = np.sqrt(dist)

##    for i in dataCleaned:
##        print(i)
##    print(dist)

    out = [dataCleaned.pop(0)]
    for i in range(0, n): # Find n closest neighbours
        index = np.argmin(dist)
        out.append(dataCleaned.pop(index))
        dist = np.delete(dist,index)


##    for i in out:
##        print(i)
    return out

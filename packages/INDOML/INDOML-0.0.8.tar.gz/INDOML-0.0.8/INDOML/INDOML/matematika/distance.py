import numpy as np

def euclidian_distance(x:np.ndarray,y:np.ndarray)->float:
    delta = x-y
    square = delta**2  
    return np.sqrt(np.sum(square))

def kuadrat_jarak(x:np.ndarray,y:np.ndarray)->float:
    return euclidian_distance(x,y)**2
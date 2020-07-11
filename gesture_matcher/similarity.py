import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import cosine


def calculate(data_1, data_2):
    r1 = []
    for vector in data_1:
        tuple = vector.to_tuple()
        r1.append((tuple[0] + 1, tuple[1] + 1, tuple[2] + 1))

    r2 = []
    for vector in data_2:
        tuple = vector.to_tuple()
        r2.append((tuple[0] + 1, tuple[1] + 1, tuple[2] + 1))

    distance, path = fastdtw(np.array(r1), np.array(r2), dist=cosine)
    print(distance)
    return distance

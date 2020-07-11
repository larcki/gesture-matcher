import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import cosine


def calculate(data_1, data_2):
    r1 = to_tuple(normalize(data_1))
    r2 = to_tuple(normalize(data_2))
    distance, path = fastdtw(np.array(r1), np.array(r2), dist=cosine)
    print(distance)
    return distance


def normalize(data):
    r1 = remove_leading_zeros(data)
    normalized = remove_leading_zeros(reversed(r1))
    normalized.reverse()
    return normalized


def to_tuple(data):
    return map(lambda vector: (vector.x + 1, vector.y + 1, vector.z + 1), data)


def remove_leading_zeros(data):
    normalized = []
    point_identified = False
    for vector in data:
        if point_identified or vector.magnitude != 0:
            point_identified = True
            normalized.append(vector)
    return normalized

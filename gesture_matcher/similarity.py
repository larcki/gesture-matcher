import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import cosine


def calculate_2(data_1, data_2):
    thumn = map(lambda frame: frame.thumb, data_1)
    thumb_s = calculate(thumn, map(lambda frame: frame.thumb, data_2))
    index_s = calculate(map(lambda frame: frame.index, data_1), map(lambda frame: frame.index, data_2))
    middle_s = calculate(map(lambda frame: frame.middle, data_1), map(lambda frame: frame.middle, data_2))
    ring_s = calculate(map(lambda frame: frame.ring, data_1), map(lambda frame: frame.ring, data_2))
    pinky_s = calculate(map(lambda frame: frame.pinky, data_1), map(lambda frame: frame.pinky, data_2))
    palm = calculate(map(lambda frame: frame.palm, data_1), map(lambda frame: frame.palm, data_2))
    palm_direction = calculate(map(lambda frame: frame.palm_direction, data_1), map(lambda frame: frame.palm_direction, data_2))
    print thumb_s, index_s, middle_s, ring_s, pinky_s, palm, palm_direction
    return palm_direction

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

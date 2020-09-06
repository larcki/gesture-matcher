import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import cosine, euclidean


class PositionNormalizer:

    def __init__(self, initial_pos_1, initial_pos_2):
        self.initial_pos_1 = initial_pos_1
        self.initial_pos_2 = initial_pos_2


def calculate(data_1, data_2):
    initial_pos_1 = initial_position(data_1)
    initial_pos_2 = initial_position(data_2)
    position_normalizer = PositionNormalizer(initial_pos_1, initial_pos_2)

    thumb = resolve_vector_array_and_calculate_distances(data_1, data_2, lambda frame: frame.thumb, position_normalizer)
    index = resolve_vector_array_and_calculate_distances(data_1, data_2, lambda frame: frame.index, position_normalizer)
    middle = resolve_vector_array_and_calculate_distances(data_1, data_2, lambda frame: frame.middle,
                                                          position_normalizer)
    ring = resolve_vector_array_and_calculate_distances(data_1, data_2, lambda frame: frame.ring, position_normalizer)
    pinky = resolve_vector_array_and_calculate_distances(data_1, data_2, lambda frame: frame.pinky, position_normalizer)
    palm = resolve_vector_array_and_calculate_distances(data_1, data_2, lambda frame: frame.palm, position_normalizer)

    similarity, total = weighted_similarity(thumb, index, middle, ring, pinky, palm)
    print '--'
    print 'Distance: ' + str(total)
    print 'Result: ' + str(similarity)
    return similarity


def initial_position(data):
    palm_data = map(lambda frame: frame.palm, data)
    return next(vector for vector in palm_data if vector.magnitude != 0)


def resolve_vector_array_and_calculate_distances(data_1, data_2, value_pick, normalizer):
    vectors_1 = map(lambda frame: value_pick(frame), data_1)
    vectors_2 = map(lambda frame: value_pick(frame), data_2)
    return calculate_distance_for_vector_arrays(vectors_1, vectors_2, normalizer)


def calculate_distance_for_vector_arrays(vector_array_1, vector_array_2, normalizer):
    normalized_tuples_1 = normalize_position(remove_leading_trailing_zeros(vector_array_1), normalizer.initial_pos_1)
    normalized_tuples_2 = normalize_position(remove_leading_trailing_zeros(vector_array_2), normalizer.initial_pos_2)
    distance = calculate_dtw_distance(normalized_tuples_1, normalized_tuples_2)
    return distance


def calculate_dtw_distance(tuples_1, tuples_2):
    distance, path = fastdtw(np.array(tuples_1), np.array(tuples_2), dist=euclidean)
    print(distance)
    return distance


def remove_leading_trailing_zeros(data):
    removed = remove_leading_zeros(reversed(remove_leading_zeros(data)))
    removed.reverse()
    return removed


def remove_leading_zeros(data):
    normalized = []
    point_identified = False
    for vector in data:
        if point_identified or vector.magnitude != 0:
            point_identified = True
            normalized.append(vector)
    return normalized


def normalize_position(data, initial_pos):
    normals = map(lambda vector: vector, data)
    rounded = map(lambda vector: (
        round(vector.x, 10) + fraction(), round(vector.y, 10) + fraction(), round(vector.z, 10) + fraction()), normals)

    pos_normalized = map(lambda t: (t[0] - initial_pos.x, t[1] - initial_pos.y, t[2] - initial_pos.z), rounded)
    return pos_normalized


def fraction():
    return 1


def weighted_similarity(thumb_s, index_s, middle_s, ring_s, pinky_s, palm):
    total = thumb_s + index_s + middle_s + ring_s + pinky_s + palm
    return weighted_similarity_for_one(total), total


def weighted_similarity_for_one(total):
    if total < 50000:
        result = 1.0 - (float(total) / 50000) / 10
    elif total < 100000:
        result = 45000 / float(total)
    else:
        result = 40000 / float(total)
    return round(result, 2)

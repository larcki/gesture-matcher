import unittest

from gesture_matcher import similarity
from gesture_matcher.recorder import GestureFrame
from gesture_matcher.similarity import PositionNormalizer
from leap.Leap import Vector


def vector(x=0, y=0, z=0):
    created_vector = Vector()
    created_vector.x = x
    created_vector.y = y
    created_vector.z = z
    return created_vector


def create_frame(thumb, index, middle, ring, pinky, palm, palm_direction):
    frame = GestureFrame()
    frame.thumb = thumb
    frame.index = index
    frame.middle = middle
    frame.ring = ring
    frame.pinky = pinky
    frame.palm = palm
    frame.palm_direction = palm_direction
    return frame


class Testing(unittest.TestCase):

    def test_normalize_position(self):
        initial_position = vector(10, 20, 15)
        result = similarity.normalize_position([
            vector(10, 15, 25),
            vector(0, -5, 100)],
            initial_position)

        self.assertEqual([(1, -4, 11), (-9, -24, 86)], result)

    def test_remove_leading_trailing_zeros(self):
        data = [
            vector(),
            vector(1, 2, 3),
            vector(),
            vector(0, 1, 0),
            vector(),
            vector()
        ]
        result = similarity.remove_leading_trailing_zeros(data)
        self.assertEqual([
            vector(1, 2, 3),
            vector(0, 0, 0),
            vector(0, 1, 0)
        ], result)

    def test_calculate_distance_for_vector_arrays_should_normalize_positions(self):
        initial_position_for_1 = vector(10, 15, 10)
        initial_position_for_2 = vector(20, 15, 0)
        normalizer = PositionNormalizer(initial_position_for_1, initial_position_for_2)

        result = similarity.calculate_distance_for_vector_arrays(
            [vector(10, 15, 10), vector(20, 10, 30)],
            [vector(20, 15, 0), vector(30, 10, 20)], normalizer)

        self.assertEqual(0, result)

    def test_calculate_dtw_distance_should_warp_time(self):
        result = similarity.calculate_dtw_distance(
            [(10, 10, 10), (20, 20, 20), (40, 40, 40)],
            [(10, 10, 10), (20, 20, 20), (20, 20, 20), (40, 40, 40)])
        # 3600 max distance X 6 every vector = 21000
        self.assertEqual(0, result)

    def test_calculate_dtw_distance_should_give_distance(self):
        result = similarity.calculate_dtw_distance(
            [(10, 11, 10), (10, 11, 10)],
            [(10, 10, 10), (11, 11, 10)])
        # max distance about 8 mil, 400 (no of frames) X 3600 (max distance of vector) X 6 (no of measures)
        self.assertEqual(0, result)

    def test_weighted_similarity(self):
        self.assertEqual(1, similarity.weighted_similarity_for_one(0))
        self.assertEqual(1, similarity.weighted_similarity_for_one(1000))
        self.assertEqual(0.94, similarity.weighted_similarity_for_one(30000))
        self.assertEqual(0.91, similarity.weighted_similarity_for_one(45000))
        self.assertEqual(0.90, similarity.weighted_similarity_for_one(49000))
        self.assertEqual(0.90, similarity.weighted_similarity_for_one(50000))
        self.assertEqual(0.88, similarity.weighted_similarity_for_one(51000))
        self.assertEqual(0.82, similarity.weighted_similarity_for_one(55000))
        self.assertEqual(0.75, similarity.weighted_similarity_for_one(60000))
        self.assertEqual(0.69, similarity.weighted_similarity_for_one(65000))
        self.assertEqual(0.64, similarity.weighted_similarity_for_one(70000))
        self.assertEqual(0.4, similarity.weighted_similarity_for_one(100000))
        self.assertEqual(0.2, similarity.weighted_similarity_for_one(200000))
        self.assertEqual(0.04, similarity.weighted_similarity_for_one(1000000))
        self.assertEqual(0.02, similarity.weighted_similarity_for_one(2000000))


if __name__ == '__main__':
    unittest.main()

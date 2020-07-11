import unittest

from gesture_matcher import similarity
from leap.Leap import Vector


def create_vector(x=0, y=0, z=0):
    vector = Vector()
    vector.x = x
    vector.y = y
    vector.z = z
    return vector


class Testing(unittest.TestCase):

    def test_normalization(self):
        data = [
            create_vector(),
            create_vector(1, 2, 3),
            create_vector(),
            create_vector(0, 1, 0),
            create_vector(),
            create_vector()
        ]
        result = similarity.normalize(data)
        self.assertEqual(result, [
            create_vector(1, 2, 3),
            create_vector(),
            create_vector(0, 1, 0)
        ])

    def test_to_tuple(self):
        data = [
            create_vector(1, 2, 3),
            create_vector(0, 1, 0),
        ]
        result = similarity.to_tuple(data)
        self.assertEqual(result, [(2, 3, 4), (1, 2, 1)])


if __name__ == '__main__':
    unittest.main()

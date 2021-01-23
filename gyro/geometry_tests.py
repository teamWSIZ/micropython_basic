import unittest
from math import pi

from gyro.geometry import *


class TestSum(unittest.TestCase):

    def lists_almost_equal(self, list1, list2, digits):
        for (r, l) in zip(list1, list2):
            self.assertAlmostEqual(r, l, digits)

    def test_1(self):
        self.assertAlmostEqual(norm([1, 0, 0]), 1)

    def test_2(self):
        self.assertAlmostEqual(norm([1, 0, 1]), 1.4142, 3)

    def test_3(self):
        self.lists_almost_equal(normalized([5, 0, 0]), [1, 0, 0], 3)

    def test_4(self):
        self.lists_almost_equal(parallel_component([1, 1, 2], [0, 0, 1]), [0, 0, 2], 3)

    def test_5(self):
        self.lists_almost_equal(perpendicular_component([1, 1, 2], [0, 0, 1]), [1, 1, 0], 3)

    def test_pitch_zero(self):
        self.assertAlmostEqual(pitch_angle([1, 1, 0], [0, 0, 1]), 0, 3)

    def test_pitch_pi4(self):
        self.assertAlmostEqual(pitch_angle([0, 1, 1], [0, 0, 1]), pi / 4, 3)

    def test_pitch_minus_pi4(self):
        self.assertAlmostEqual(pitch_angle([0, 1, -1], [0, 0, 1]), -pi / 4, 3)

    def test_yaw_pi_4(self):
        self.assertAlmostEqual(yaw_angle([1, 1, 0], [0, 0, 1], [1, 0, 0]), pi / 4, 3)

    def test_yaw_pi_2(self):
        self.assertAlmostEqual(yaw_angle([0, 1, 0], [0, 0, 1], [1, 0, 0]), pi / 2, 3)

    def test_yaw_pi(self):
        self.assertAlmostEqual(yaw_angle([-0.9999, 0, 0], [0, 0, 1], [1, 0, 0]), pi, 3)

    def test_yaw_minus_pi_2(self):
        self.assertAlmostEqual(yaw_angle([-0.00001, -1, 0], [0, 0, 1], [1, 0, 0]), -pi / 2, 3)

    def test_yaw_minus_pi(self):
        self.assertAlmostEqual(yaw_angle([-0.99999, -0.0001, 0], [0, 0, 1], [1, 0, 0]), -pi, 3)

    def test_yaw_rotate_pi2(self):
        v = [1, 0, 0]
        a = [0, 0, pi / 2]
        w = rotate_vector(v, a, 1000)
        self.lists_almost_equal(w, [0, 1, 0], 2)

    def test_yaw_rotate_2pi(self):
        v = [1, 0, 0]
        a = [0, 0, pi * 2]
        w = rotate_vector(v, a, 4000)
        self.lists_almost_equal(w, [1, 0, 0], 2)

    def test_roll_along_unchanged(self):
        v = [1, 0, 0]
        a = [pi / 2, 0, 0]
        w = rotate_vector(v, a, 4000)
        self.lists_almost_equal(w, [1, 0, 0], 2)

    def test_roll_y_pi4(self):
        # x y→z
        v = [0, 1, 0]
        a = [pi / 4, 0, 0]
        w = rotate_vector(v, a, 4000)
        expected_w = normalized([0, 1, 1])
        self.lists_almost_equal(w, expected_w, 2)

    def test_pitch_x_pi4(self):
        v = [1, 0, 0]
        a = [0, pi / 4, 0]
        print(get_small_rotation_matrix([0.01, 0, 0]))
        w = rotate_vector(v, a, 4000)
        expected_w = normalized([1, 0, -1])
        # print_v(w)
        # print_v(expected_w)
        self.lists_almost_equal(w, expected_w, 2)

    def test_roll_pitch_unroll(self):
        basis = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]  # fuselage=x; right_wing=y
        # roll 90 degrees "right"
        angle_l = [pi / 2, 0, 0]
        angle_g = rotation_vector_local_to_absolute(basis, angle_l)
        basis = rotate_basis(basis, angle_g, 10000)

        # pull up by 90 degrees (pitch up)
        angle_l = [0, pi / 2, 0]
        angle_g = rotation_vector_local_to_absolute(basis, angle_l)
        basis = rotate_basis(basis, angle_g, 10000)

        # roll back ("left") by -90 degrees
        angle_l = [-pi / 2, 0, 0]
        angle_g = rotation_vector_local_to_absolute(basis, angle_l)
        basis = rotate_basis(basis, angle_g, 10000)

        self.lists_almost_equal(basis[0], [0, 1, 0], 2)
        self.lists_almost_equal(basis[1], [-1, 0, 0], 2)
        # print_v(basis[0])
        # print_v(basis[1])

    def test_pitch_roll_pitch(self):
        basis = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]  # fuselage=x; right_wing=y
        # pitch "up" 90deg
        angle_l = [0, pi / 2, 0]
        angle_g = rotation_vector_local_to_absolute(basis, angle_l)
        basis = rotate_basis(basis, angle_g, 10000)

        # roll "left" 90deg
        angle_l = [-pi / 2, 0, 0]
        angle_g = rotation_vector_local_to_absolute(basis, angle_l)
        basis = rotate_basis(basis, angle_g, 10000)

        # pitch "up" 90deg
        angle_l = [0, pi / 2, 0]
        angle_g = rotation_vector_local_to_absolute(basis, angle_l)
        basis = rotate_basis(basis, angle_g, 10000)

        #result: "upside down"; fuselage along (-y), right wing along (-x)
        self.lists_almost_equal(basis[0], [0, -1, 0], 2)
        self.lists_almost_equal(basis[1], [-1, 0, 0], 2)
        # print_v(basis[0])
        # print_v(basis[1])


if __name__ == '__main__':
    unittest.main()

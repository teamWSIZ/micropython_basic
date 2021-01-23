from copy import copy, deepcopy
from math import sqrt, atan, acos, pi
from typing import List

"""
Prosty pakiet funkcji do geometrii.
Działa na 2D, 3D etc.
"""


def norm(vec) -> float:
    """
    :return: Length of `vec`
    """
    return sqrt(sum([a ** 2 for a in vec]))


def normalized(vec: List[float]) -> List[float]:
    """
    :return: Copy of `vec` normalized to 1.
    """
    n = norm(vec)
    g = [x / n for x in vec]
    return g


def scalar_product(vec_x, vec_y) -> float:
    return sum([a * b for (a, b) in zip(vec_x, vec_y)])


def vector_product_3d(a, b) -> List[float]:
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def parallel_component(vec, axis) -> List[float]:
    """
    :return: The part of `vec` which is parallel to `axis`
    """
    n_axis = normalized(axis)
    scalar = scalar_product(vec, n_axis)
    return [a * scalar for a in n_axis]


def perpendicular_component(vec, axis) -> List[float]:
    """
    :return: The part of `vec` which is perpendicular to `axis`
    """
    n_v = parallel_component(vec, axis)
    return [vv - nn for (vv, nn) in zip(vec, n_v)]


def pitch_angle(vec, up_axis) -> float:
    up = norm(parallel_component(vec, up_axis))
    if scalar_product(vec, up_axis) < 0:
        up = -up
    in_plane = norm(perpendicular_component(vec, up_axis))
    in_plane += 0.001  # avoid zero
    return atan(up / in_plane)


def yaw_angle(vec, up_axis, north_axis) -> float:
    """
    :param up_axis: select plane of measurement
    :param north_axis: yaw = 0; assumed normalized, perpendicular to up_axis
    :return: angle in (-pi,pi)
    """
    vec = normalized(perpendicular_component(vec, up_axis))  # take in-plane component only
    alpha = acos(scalar_product(vec, north_axis))
    w_axis = vector_product_3d(up_axis, north_axis)  # west
    if scalar_product(vec, w_axis) < 0:
        alpha = -alpha
    return alpha


def get_small_rotation_matrix(angle: List[float]) -> List[List[float]]:
    """
    :return: Rotation matrix for small angles; R vec_x = vec'_x (slightly rotated)

    Note: generators are selected so that positive-angle rotations act as follows:
     * z-axis rotation (yaw) changes (x->y ...)
     * x-axis rotation (roll) changes (y->z ...)
     * y-axis rotation (pitch) changes (z->x ...)
     https://www.physik.uni-bielefeld.de/~borghini/Teaching/Symmetries/12_15.pdf, page 72
    """
    r = [[1., 0, 0], [0, 1, 0], [0, 0, 1]]
    r[0][1] = -angle[2]
    r[1][0] = angle[2]
    r[1][2] = -angle[0]
    r[2][1] = angle[0]
    r[0][2] = angle[1]
    r[2][0] = -angle[1]
    return r


def rotate_vector(vec: List[float], angle: List[float], steps) -> List[float]:
    r = get_small_rotation_matrix([a / steps for a in angle])
    v = copy(vec)
    for i in range(steps):
        v = matrix_on_vector(r, v)
    return v


def rotate_basis_small_angle(basis, angle):
    r = get_small_rotation_matrix(angle)
    v_nx = matrix_on_vector(r, basis[0])
    v_ny = matrix_on_vector(r, basis[1])
    v_nz = matrix_on_vector(r, basis[2])
    # new_basis = [normalized(v_nx), normalized(v_ny), normalized(v_nz)]
    new_basis = [v_nx, v_ny, v_nz]
    return new_basis


def rotate_basis(basis, angle, steps):
    nbasis = deepcopy(basis)
    for i in range(steps):
        nbasis = rotate_basis_small_angle(nbasis, [a / steps for a in angle])
    return nbasis


def rotation_vector_local_to_absolute(basis, angle):
    """
    :param basis: (x,y,z) local basis vectors expressed in XYZ (global) basis
    :param angle: (ax,ay,az): local rotations
    :return: angle as expressed in global basis
    """
    res_angle = [0] * 3
    for i in range(3):
        for b in range(3):
            res_angle[i] += angle[b] * basis[b][i]
    return res_angle


def matrix_on_vector(matrix, vector) -> List[float]:
    n = len(vector)
    res = [0] * n
    for r in range(n):
        s = 0
        for c in range(n):
            s += matrix[r][c] * vector[c]
        res[r] = s
    return res


def matrix_multiply(m1, m2):
    """
    Matrices assumed sqare.
    """
    n = len(m1[0])
    res = [[0] * n] * n
    for r in range(n):
        for c in range(n):
            for k in range(n):
                res[r][c] += m1[r][k] * m2[k][c]
    return res


def print_v(vec):
    out: str = '('
    for v in vec:
        out += f'{v:.4f}, '
    out = out[:-2] + ')'
    print(out)


if __name__ == '__main__':
    basis = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    basis = rotate_basis(basis, [0, 0, pi / 2], 10000)  # x->y, y->(-x)
    for v in basis:
        print_v(v)
    omega = [0.05, 0, 0] # rotation around local x by 0.05 should be global rotation around y by 0.05
    omega_g = rotation_vector_local_to_absolute(basis, omega)
    print_v(omega_g)

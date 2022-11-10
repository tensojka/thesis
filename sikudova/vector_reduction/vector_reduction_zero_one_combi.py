import numpy as np
from copy import deepcopy
from math import floor
from zero_one_combination import zero_one_combination
# from integer_files import lattices_10_1


def minimum_norm(matrix):
    """
    Return norm of the shortest vector in the matrix.
    :param matrix: matrix where to find the norm
    :return: the minimal norm
    """
    rows, cols = matrix.shape
    magnitudes = []

    for i in range(rows):
        magnitudes.append(np.linalg.norm(matrix[i]))

    return min(magnitudes)


def gram_matrix(matrix):
    """
    Calculate Gram matrix of given matrix.
    :param matrix: given matrix
    :return: Gram matrix of matrix
    """
    return np.matmul(matrix, matrix.transpose())


def calculate_bc(index, matrix):
    """
    Calculates exact coefficients for matrix, for first vector coefficient = 1.
    :param index: index already defined for vector - alpha_1 = 1
    :param matrix: matrix of vectors, vectors on indexes already multiplied
    :return: array of exact coefficients
    """
    rows, cols = matrix.shape
    matrix_a = np.empty([rows - 1, rows - 1])
    matrix_b = np.empty([rows - 1, 1])
    a_index, b_index = 0, 0
    for row in range(rows):
        if row != index:
            matrix_a[a_index] = matrix[row, 1: cols]
            matrix_b[b_index] = matrix[row, 0]
            a_index += 1
            b_index += 1

    result = np.linalg.solve(matrix_a, -1 * matrix_b)
    return result


def reduce_vector(matrix: np.ndarray, dot_matrix: np.ndarray) -> object:
    """
    Find better linear combination of vectors (except the first one) to the first vector in matrix.
    :param matrix: matrix of vectors
    :param dot_matrix: gram matrix of matrix
    :return: array of vector with the minimal norm, coefficients and the minimal norm
    """
    rows, cols = matrix.shape

    # coefficients, vector of real numbers
    coefficients = calculate_bc(0, dot_matrix)

    # coefficients, vector of integers, from coefficients items - floored and ceiled
    rounded_coefficients = [[] for _ in range(len(coefficients))]
    for i in range(len(coefficients)):
        rounded_coefficients[i] = [floor(coefficients[i]), floor(coefficients[i] + 1)]

    starting_vector = [x[0] for x in rounded_coefficients]

    # norm of the first vector we want to decrease
    min_magnitude = np.linalg.norm(matrix[0])

    best_vectors = [deepcopy(matrix[0])]
    best_coefficients = [[0 for _ in range(rows - 1)]]

    # generate numbers to create good linear combinations
    zero_one_array = zero_one_combination(rows - 1)
    temp_vector = deepcopy(matrix[0])
    vector = [0 for _ in range(rows - 1)]
    for i in range(rows - 1):
        temp_vector += starting_vector[i] * matrix[i + 1]

    # all coefficients generated with the help of good sorted zero_one array
    for each in zero_one_array:
        # coeff = deepcopy(starting_vector)
        if each < 0:
            temp_vector -= matrix[abs(each) + 1]
            vector[abs(each)] = 0
        else:
            temp_vector += matrix[abs(each) + 1]
            vector[each] = 1
        if np.linalg.norm(temp_vector) < min_magnitude:  # shortest vector found
            best_vectors = [deepcopy(temp_vector)]
            best_coefficients = [np.add(vector, starting_vector)]
            min_magnitude = np.linalg.norm(temp_vector)
        elif np.linalg.norm(temp_vector) == min_magnitude:  # vector of the same norm found
            best_vectors.append(deepcopy(temp_vector))
            best_coefficients.append(np.add(vector, starting_vector))

    # assert to check the norm
    for i in range(len(best_vectors)):
        assert (min_magnitude == np.linalg.norm(best_vectors[i]))

    return best_vectors, best_coefficients, min_magnitude


def main_reduce_function(matrix):
    """
    Iterates over all vectors and compares norms of vectors from reduce_function.
    :param matrix: matrix of vector
    :return: array of shortest found vectors, relevant coefficients and the minimal norm
    """

    rows, cols = matrix.shape

    # variables for resulting shortest vector, its norm and its coefficients
    result_vector = []
    best_coefficients = []
    min_magnitude = minimum_norm(matrix)

    # Gram matrix
    dot_matrix = gram_matrix(matrix)

    for i in range(rows):
        # swapping vector, aim: i-th vector to be first in matrix
        if i != 0:
            temp = deepcopy(matrix[0])
            matrix[0] = matrix[i]
            matrix[i] = temp
            dot_matrix = gram_matrix(matrix)

        # find the best linear combination for i-th vector
        best_vector, coefficients, magnitude = reduce_vector(matrix, dot_matrix)

        # insert alpha_1 = 1 to the i-th (now first in the matrix) vector
        for k in range(len(coefficients)):
            coefficients[k] = np.insert(coefficients[k], 0, 1)

        # shift coefficients
        for j in range(len(coefficients)):
            coefficients[j][0:i + 1] = list(np.roll(coefficients[j][0:i + 1], i))

        if magnitude < min_magnitude:  # shorter vector found
            result_vector = deepcopy(best_vector)
            best_coefficients = deepcopy(coefficients)
            min_magnitude = magnitude
        elif magnitude == min_magnitude:  # vector of the same norm found
            for each in best_vector:
                result_vector.append(deepcopy(each))
            for each in coefficients:
                best_coefficients.append(deepcopy(each))

    # shift vectors to the original order
    matrix = np.roll(matrix, -1, axis=0)

    # check correctness of all linear combinations
    for each in best_coefficients:
        check_result = np.zeros(cols)
        for i in range(rows):
            check_result += each[i] * matrix[i]
        is_ok = False
        for vector in result_vector:
            if np.allclose(check_result, vector):
                is_ok = True
            if np.allclose((-1) * check_result, vector):
                is_ok = True
        if not is_ok:
            print("ERROR!!!")
            exit(1)

    return min_magnitude, result_vector, best_coefficients

lattice_1 = Matrix([[4, 3, -17, -22, -3, -45, 2, 47, 44, -48],
                      [23, 36, 24, -8, 6, 21, 29, 3, 21, -9],
                      [-42, -29, -45, -8, -25, 6, -11, 39, 43, 18],
                      [31, 33, -35, -40, -14, -13, -40, 18, -2, 39],
                      [12, 16, 41, 5, -13, -26, 20, -47, -19, 20],
                      [40, 16, 28, -5, -33, -13, -43, -22, 33, -8],
                      [0, 13, 6, -44, -19, -48, -36, -24, 34, 3],
                      [-27, 23, -35, 47, 12, -30, 36, -48, 20, -16],
                      [-50, -45, 41, -49, -17, 9, 11, -7, -35, -20],
                      [-19, -1, 24, -25, 48, 36, 18, 49, 24, 46]])

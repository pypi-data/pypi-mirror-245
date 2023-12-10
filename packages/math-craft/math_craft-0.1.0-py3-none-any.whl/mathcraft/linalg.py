import numpy as np


class Vector(np.ndarray):
    def __new__(cls, input_array):
        # Create a new instance of the class with the input_array
        obj = np.asarray(input_array).view(cls).reshape(-1, 1)
        return obj

    def norm(self):
        # Calculate and return the magnitude of the vector
        return np.linalg.norm(self)


class Ones(np.ndarray):
    def __new__(cls, size: int):
        # Create a new instance of the class with the input_array
        obj = np.ones(shape=(size, 1)).view(cls)
        return obj


class Matrix(np.ndarray):
    def __new__(cls, input_array):
        # Create a new instance of the class with the input_array
        obj = np.asarray(input_array).view(cls)
        return obj

    def det(self):
        # Calculate and return the determinant of the matrix
        return np.linalg.det(self)

    def T(self):
        # Return the transpose of the matrix
        return np.transpose(self)
    
    def inv(self):
        return np.linalg.inv(self)

    def pinv(self):
        return np.linalg.pinv(self)
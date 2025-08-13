import numpy as np
from numpy._typing import NDArray

class Calcolous:

    @staticmethod
    def dct2(f_mat: NDArray[np.float64]):

        n = np.shape(f_mat)[0]

        # calcolo la matrice DCT monodimensionale
        D = Calcolous.__compute_dct(n)

        c_mat = f_mat.copy()

        # DCT1 per colonne
        for j in range(n):
            c_mat[:, j] = np.dot(D, c_mat[:, j])

        # DCT1 per righe
        for j in range(n):
            c_mat[j, :] = np.dot(D, c_mat[j, :])

        return c_mat

    @staticmethod
    def __compute_dct(n: int):

        # creo il vettore alpha basandomi su n
        alpha_vect = np.zeros(n, dtype=float)
        alpha_vect[0] = n ** (-0.5)
        alpha_vect[1:] = n ** (-0.5) * np.sqrt(2.0)

        D = np.zeros((n, n), dtype=float)
        for k in range(n):
            for i in range(n):
                D[k, i] = alpha_vect[k] * np.cos((k) * np.pi * (2 * (i + 1) - 1) / (2 * n))

        return D

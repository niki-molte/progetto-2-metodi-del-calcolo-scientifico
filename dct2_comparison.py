import time

import numpy as np
from numpy.typing import NDArray

from scipy.fft import dctn, dct
import matplotlib.pyplot as plt

from core.my_dct2 import Calcolous


class DctUtilities:

    def __init__(self, max_n: int):

        if max_n <= 0:
            raise ValueError("max_n deve essere maggiore di 0")

        self.max_n = max_n


    def test_dct(self, f: NDArray[np.float64]) -> bool:
        ref = np.array([4.019902051045523e+02, 6.600019905532511e+00, 1.091673654442963e+02, -1.127855785717513e+02,
                        6.540737725975565e+01, 1.218313980366680e+02, 1.166564885548655e+02, 2.880040721783050e+01],
                       dtype=float)

        dct1 = dct(f[0, :], type=2, norm='ortho')

        if np.allclose(dct1, ref):
            return True

        return False

    def test_dct2(self, f: NDArray[np.float64]) -> bool:
        ref = np.array([
            [1.118750000000000e+03, 4.402219262301787e+01, 7.591905032609426e+01, -1.385724109970731e+02,
             3.500000000000028e+00, 1.220780551880306e+02, 1.950438676236296e+02, -1.016049059279537e+02],
            [7.719007901879010e+01, 1.148682059069701e+02, -2.180144211456541e+01, 4.136413505703621e+01,
             8.777205976079186e+00, 9.908296204231640e+01, 1.381715157321194e+02, 1.090927953407787e+01],
            [4.483515365361005e+01, -6.275244638273558e+01, 1.116141142168384e+02, -7.637896579814382e+01,
             1.244221596807072e+02, 9.559841936381827e+01, -3.982879694884997e+01, 5.852376699413913e+01],
            [-6.998366474768355e+01, -4.024089448027942e+01, -2.349705083457044e+01, -7.673205936982573e+01,
             2.664577495045286e+01, -3.683282895356626e+01, 6.618914845485334e+01, 1.254297306179912e+02],
            [-1.090000000000000e+02, -4.334308566057378e+01, -5.554369078865144e+01, 8.173470828327527e+00,
             3.025000000000001e+01, -2.866024373369901e+01, 2.441498223361492e+00, -9.414370254649863e+01],
            [-5.387835905170846e+00, 5.663450089125683e+01, 1.730215190411498e+02, -3.542344938713219e+01,
             3.238782492363563e+01, 3.345767275218619e+01, -5.811678637187249e+01, 1.902256148701118e+01],
            [7.884396931190857e+01, -6.459240955238300e+01, 1.186712030511500e+02, -1.509048397585812e+01,
             -1.373169278726720e+02, -3.061966628119865e+01, -1.051141142168384e+02, 3.981304970688294e+01],
            [1.978824382848894e+01, -7.818134089948808e+01, 9.723118598351341e-01, -7.234641800960696e+01,
             -2.157816325036089e+01, 8.129990354778818e+01, 6.371037820527631e+01, 5.906180710669425e+00]
        ], dtype=float
        )

        dct2 = dctn(f, type=2, norm='ortho')

        if np.allclose(dct2, ref):
            return True

        return False

    def test_implemented_dct2(self, scipy_dct: NDArray[np.float64], my_dct: NDArray[np.float64]) -> bool:
        if np.allclose(scipy_dct, my_dct):
            return True

        return False

    def __generate_matrices(self, step=10):
        for n in range(step, self.max_n + 1, step):
            mat = np.random.randint(0, 256, size=(n, n), dtype=np.uint8)
            yield n, mat

    def __compare_dct(self):

        result = []

        for n, matrix in self.__generate_matrices():

            start_my_dct = time.time()
            Calcolous.dct2(matrix)
            stop_my_dct = time.time()
            my_dct = stop_my_dct - start_my_dct

            start_dct = time.time()
            dctn(matrix, type=2, norm='ortho')
            stop_dct = time.time()
            library_dct = stop_dct - start_dct

            partial_result = [my_dct, library_dct, n]
            result.append(partial_result)

        return result

    def dct_comparison(self):

        results = self.__compare_dct()

        my_dct_time = [element[0] for element in results]
        library_dct_time = [element[1] for element in results]
        ns = [element[2] for element in results]

        print(f"\n \nTempo totale di computazione my_dct {np.sum(my_dct_time)} (s)")
        print(f"Tempo totale di computazione library_dct {np.sum(library_dct_time)} (s)")

        plt.figure()
        plt.plot(ns, my_dct_time, color="blue", label="my DCT")
        plt.plot(ns, library_dct_time, color="green", label="library DCT")

        ref_my_dct = [n ** 3 / 1e12 for n in ns]
        ref_library_dct = [(n ** 2 * np.log(n)) / 1e12 for n in ns]

        #ref_my_dct = [n**3 for n in ns]
        #ref_library_dct = [(n**2)*np.log(n) for n in ns]

        # Fattori di scala per allineare la complessità teorica
        #c_my = my_dct_time[0] / ns[0] ** 3
        #c_lib = library_dct_time[0] / (ns[0] ** 2 * np.log(ns[0]))

        # Curve teoriche traslate
        #ref_my_dct = [c_my * n ** 3 for n in ns]
        #ref_library_dct = [c_lib * n ** 2 * np.log(n) for n in ns]

        #plt.plot(ns, ref_my_dct, color="red", linestyle='-.', label="my DCT reference (N^3)")
        #plt.plot(ns, ref_library_dct, color="red", linestyle='--', label="library DCT reference (N^2Log(N))")

        plt.title("Confronto in termini di tempo tra \n DCT implementata e DCT da libreria")
        plt.ylabel("Tempo(s)")
        plt.xlabel("Dimensione della matrice")
        plt.yscale('log')

        plt.legend()
        plt.show()









# blocco 8x8 su cui vengono eseguiti i test per
# dimostrare la correttezza della DCT e DCT2
# implementata nella libreria
block = np.array([
    [231, 32, 233, 161, 24, 71, 140, 245],
    [247, 40, 248, 245, 124, 204, 36, 107],
    [234, 202, 245, 167, 9, 217, 239, 173],
    [193, 190, 100, 167, 43, 180, 8, 70],
    [11, 24, 210, 177, 81, 243, 8, 112],
    [97, 195, 203, 47, 125, 114, 165, 181],
    [193, 70, 174, 167, 41, 30, 127, 245],
    [87, 149, 57, 192, 65, 129, 178, 228]
], dtype=float)

util = DctUtilities(max_n=1500)

# calcolo la DCT2 con la libreria implementata
dct2_my = Calcolous.dct2(f_mat=block)

# calcolo la DCT2 con la funzione di scipy
dct2 = dctn(block, type=2, norm='ortho')

print(f"La DCT implementata da scipy è uguale a quella implementata da MATLAB? {util.test_dct(block)}")
print(f"La DCT2 implementata da scipy è uguale a quella implementata da MATLAB? {util.test_dct2(block)}")

print(f"La DCT2 implementata da scipy è uguale a quella implementata da noi? {util.test_implemented_dct2(dct2, dct2_my)}")

util.dct_comparison()
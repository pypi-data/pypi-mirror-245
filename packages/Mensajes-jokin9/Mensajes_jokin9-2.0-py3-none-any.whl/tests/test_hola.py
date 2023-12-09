import unittest
import numpy as np
from mensajes.hola.saludos import generarArray

class PruebasHola(unittest.TestCase):

    def testGenerarArray(self):
        np.testing.assert_array_equal(
            np.array([0,1,2,3,4,5]),
            generarArray(6)
        )


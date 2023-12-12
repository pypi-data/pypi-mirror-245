#importamos el codigo completo del archivo saludos
import unittest
import numpy as np
from mensajes.hola.saludos import generar_array

class PruebasHola(unittest.TestCase):
    def test_generar_array(self):
        np.testing.assert_array_equal(
            np.array([0,1,2,3,4,5]),
            generar_array(6))

from mensajes.hola.saludos import *
from mensajes.adios.despedidas import *

#podemos importar definiciones escribiendolas o todas de una con un asterisco
#from saludos importar saludar, despedir, nombrar
#from saludos importar *
saludar()
Saludo()

despedir()
Despedida()

#los paquetes son colecciones de modulos



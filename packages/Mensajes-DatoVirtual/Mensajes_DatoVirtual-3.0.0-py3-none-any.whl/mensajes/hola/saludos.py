import numpy as np

def saludar():
    print("Hola te saludo desde saludos.saludar()")

#almacena en la ejecucion de un programa un nombre de script

def prueba():
    print("esto es una prueba de actualizacion")

if __name__ == "__main__":
    saludar()

def generar_array(numeros):
    return np.arange(numeros)


#creamos una clase
class Saludo:
    def __init__(self): #llamamos al metodo constructor
        print("Hola te saludo desde Saludo.__init__")

if __name__ == "__main__":
    print(generar_array(5))
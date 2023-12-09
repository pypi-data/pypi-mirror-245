import numpy as np

def saludar():
    print("Hola, te saludo desde saludos.saludar()")

def prueba():
    print("Esto es una prueba de la nueva version.")

def prueba2():
    print("Esto es una prueba de la 2.1")

def generarArray(numeros):
    return np.arange(numeros) # genera un array dinamicamente

class Saludo:
    
    def __init__(self):
        print("Hola, te saludo desde Saludo.__init__()")
        

# Esto hace que al importarlo no se ejecute esta pieza de codigo
if __name__ == "__main__":
    print(generarArray(5))
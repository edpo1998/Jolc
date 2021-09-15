'''
    Esta clase sirve para recibir como parametro el nombre de un archivo 
    en la consolo para posteriormente realizar la interpretacion
    de este..
'''
import jolc
import sys

# Subir el limite de recursion de python
sys.setrecursionlimit(6000)

if len(sys.argv) == 1:
    print("File: %s "%(__file__))
else:   
    with open(sys.argv[1]) as f:
        jolc.execute(f.read())
#import sys,pygame
#import Image
from math import *
import math
from PIL import Image
from sys import argv # Importe para tabajar con argumentos
import time


def main():
  foto1 = contraste()

def contraste():
  #toma imagen en escala de grises
  inicio = time.time()
  image1 = Image.open("nueva.png")
  pixels = image1.load()
  ancho,alto = image1.size
  minimo = int(argv[2]) #toma un valor umbral minimo
  for i in range(ancho):
    for j in range(alto):
      a = pixels[i,j]
      escala = int((a[0] + a[1] + a[2])/3)			
      pixels[i,j] = (escala,escala, escala)
      if pixels[i,j][1] < minimo:
        p=0
      else:
        p= 255
      pixels[i,j]=(p,p,p)
      fin = time.time()
      tiempo_t = fin - inicio
      print("Tiempo que tardo en ejecutarse binzarizar = "+str(tiempo_t)+" segundos")
      print(i)
      print(j)

  new = 'contraste.png'
  image1.save(new)
  return new

if __name__ == "__main__":
    main()

#Pedir megapixeles
#Pedir dimensiones

#******Los pasos son: 
#
#1 - Escala de grises
#2 - Filtro (de los vecinos)
#3 - Convolucion
#4 - Normalizacion (por diferencia)
#5 - Binarizacion

#Obtener resoluciones
#Umbrales
import pygame
from pygame.locals import*
from PIL import Image,ImageTk
from math import *
import sys
import numpy
import time
import random
from sys import argv
#import Image, ImageTk
#import Tkinter

def main():  	
	
	acumulado1 = 0
	acumulado2 = 0
	acumulado3 = 0
	acumulado4 = 0

	transformar()
	filtrada()
	#diferencia()
	convolucion()
	umbrales()
	formas()
	#salPimienta()
	#quitarSalPimienta()
	#eleccion = 0	

	#pygame.init()
	#screen = pygame.display.set_mode((800, 680))
	#pygame.display.set_caption("Bla")

	#fondo = pygame.image.load("mina.jpeg").convert()
	#Posicion
	#screen.blit(fondo, (0, 0))
	#pygame.display.flip()
		#eleccion = int(raw_input('Ingresa 1 para escala de grises y 2 para umbrales: '))

	#while True:
	#	for event in pygame.event.get():
	#		if event.type == pygame.QUIT:
	#			sys.exit()

#Funcion para escala de grises
#Se accede a ella presionando 1
def transformar():
	#tiempoInicial = time.time()
	i = 0
	x = 0
	y = 0
	im = Image.open("mina.jpeg")
	
	for x in range(im.size[0]):
		for y in range(im.size[1]):
			pix = im.load()
			tupla = pix[x, y]
	
			a = tupla[0]
			b = tupla[1]
			c = tupla[2]
			
			prom = int((a+b+c)/3)
			newTupla = (prom,prom,prom)
			im.putpixel((x, y), newTupla)			

			#print tupla, "--", a,",",b,",",c
	im.save('meh.jpg')
	#tiempoFinal = time.time()
	#transcurso = tiempoFinal - tiempoInicial
	#print "Tiempo de escala de grises = ", transcurso 

def filtrada(): #Filtrada por el metodo de los vecinos
	#tiempoInicial = time.time()
	i = 0
	x = 0
	y = 0
	im = Image.open("meh.jpg")
	width, height = im.size
	pix = im.load() 
	promedio = 0
	width = width-1
	height = height-1

	#x = j y y = i
	for x in range(height):
		for y in range(width):
			#esquina superior izquierda
			if y == 0 and x == 0:
				promedio = (sum(pix[y + 1,x])/3 + sum(pix[y,x + 1])/3 + sum(pix[y,x])/3)/3
			#esquina superior derecha
			if y == width and x == 0:
				promedio = (sum(pix[y,x+1])/3 + sum(pix[y-1,x])/3 + sum(pix[y,x])/3)/3

			if y == 0 and x == height:
					promedio = (sum(pix[y,x-1])/3 + sum(pix[y+1,x])/3 + sum(pix[y,x])/3)/3

			if y == height and x == width:
					promedio = (sum(pix[y - 1,x])/3 + sum(pix[y,x - 1])/3 + sum(pix[y,x])/3)/3

			if y > 0 and y < width and x == 0:
				promedio = (sum(pix[y+1,x])/3 + sum(pix[y-1,x])/3 +sum(pix[y,x+1])/3+ sum(pix[y,x])/3)/4
		
			if y > 0 and y < width and x == height:
				promedio = (sum(pix[y -1,x])/3 + sum(pix[y,x-1])/3 +sum(pix[y+1,x])/3+ sum(pix[y,x])/3)/4

			if x >0 and x <height and y == 0:
				promedio = (sum(pix[y+1,x])/3 + sum(pix[y,x-1])/3 +sum(pix[y,x +1])/3+ sum(pix[y,x])/3)/4

			if y == width and x >0 and x < height:
				promedio = (sum(pix[y - 1,x])/3 + sum(pix[y,x-1])/3 + sum(pix[y,x +1])/3+ sum(pix[y,x])/3)/4

			if y > 0 and y< width and x>0 and x< height:
				promedio = (sum(pix[y,x])/3 + sum(pix[y + 1,x])/3 + sum(pix[y - 1,x])/3 + sum(pix[y,x + 1])/3 + sum(pix[y,x -1])/3)/5	
	


			#-----------------------------
			#tupla = pix[x, y]
			promedio = int(promedio)
			a = promedio
			b = promedio
			c = promedio	
			'''
			a = tupla[0]
			b = tupla[1]
			c = tupla[2]
			'''
			#prom = int((a+b+c)/3)
			pix[y, x] = (a,b,c)
			#tup = pix[]
			#im.putpixel((y, y), pix)			

			#print tupla, "--", a,",",b,",",c
	im.save('meh2.jpg')
	#tiempoFinal = time.time()
	#transcurso = tiempoFinal - tiempoInicial
	#print "Tiempo transcurrido durante la filtracion = ", transcurso


def diferencia(): #O normalizacion
	#tiempoInicial = time.time()
	imagen1 = Image.open("meh.jpg")
	imagen2 = Image.open("meh2.jpg")
	width, height = imagen1.size
	pix = imagen1.load()
	pix2 = imagen2.load()

	for y in range(width):
		for x in range(height):
			(a,b,c) = pix[y, x]
			(d,e,f) = pix2[y, x]
			promedio = a+b+c/3
			promedio1 = d+e+f/3
			promedio2 = promedio - promedio1

			if promedio2 > 115:
				promedio2 = 255
			else:
				promedio2 = 0
			a = promedio2
			b = promedio2
			c = promedio2	 
			pix[y, x] = (a,b,c)
	imagen1.save("meh3.jpg")
	#tiempoFinal = time.time()
	#transcurso = tiempoFinal - tiempoInicial
	#print "Tiempo transcurrido durante la normalizacion = ", transcurrido

def convolucion():
	#tiempoInicial = time.time()
	'''         ---       ---                     ---    ---
						| -1  0  1  |		     | 1  2  1  |
	SOBEL: Sx = | -2  0  2  |		Sy = | 0  0  0  |
								| -1  0  1  |		     |-1 -2 -1  |
							---       ---                     ---    ---

	S = raiz(Sx2+Sy2)

	'''	
	
	im = Image.open("meh2.jpg")
	width, height = im.size
	pix = im.load()
	resultado = 0
	gradienteX = ([-1, 0, 1], [-2, 0, 2], [-1, 0, 1])  #Valores establecidos por medio del operador Sobel
	gradienteY = ([1, 2, 1], [0, 0, 0], [-1, -2, -1])  #Para gradiente de y, el de arriba es el gradiente de x.
	sumasX = 0
	sumasY = 0 	

	for x in range(height):
		for y in range(width):
			sumasX = 0
			sumasY = 0
			if x != 0 and y != 0 and y != width and x != height: #Para obtener un centrado de la mascara, evita la primera linea de pixeles de la imagen por los 4 lados
				#x = a
				#y = b			
				for a in range(3): #Debido a que la matriz de los gradientes es de 3x3
					for b in range(3):
						try:
							productosGX = gradienteX[a][b]*pix[y+b, x+a][1] #Obteniendo el valor de gradiente X
							productosGY = gradienteY[a][b]*pix[y+b, x+a][1]	#Obteniendo el valor de gradiente Y
			
						except:
							productosGX = 0
							productosGY = 0
					
						sumasX = productosGX+sumasX #Adicionando los valores del gradiente X
						sumasY = productosGY+sumasY #Adicionando los valores del gradiente Y
			
				potenciaGradienteX = pow(sumasX, 2) #Obteniendo el cuadrado del gradiente X
				potenciaGradienteY = pow(sumasY, 2) #Obteniendo el cuadrado del gradiente Y
				Gradiente = int(sqrt(potenciaGradienteX+potenciaGradienteY)) #Para obtener el gradiente por medio de los componentes x, y
				#resultado = Gradiente

				if Gradiente > 255: #Por si se pasan los valores
					Gradiente = 255

				if Gradiente < 0: #Para estar dentro del rango (0, 255) 
					Gradiente = 0
		
				pix[y,x] = (Gradiente, Gradiente, Gradiente) # Creando el pixel nuevo con el gradiente obtenido			
	
	im.save('meh4.jpg')					
	#tiempoFinal = time.time()	
	#transcurrido = tiempoFinal - tiempoInicial
	#print "Tiempo transcurrido durante la convolucion = ", transcurrido
	
#Funcion umbrales
#Se accede a ella presionando 2
def umbrales():
	#tiempoInicial = time.time()
	i = 0
	x = 0  
	y = 0
	umbInferior = 77
	umbSuperior = 177
	im = Image.open("meh4.jpg")
	
	for x in range(im.size[0]):
		for y in range(im.size[1]):
			pix = im.load()
			tupla = pix[x, y]
	
			a = tupla[0]
			b = tupla[1]
			c = tupla[2]
			
			prom = int((a+b+c)/3)
			if prom < umbInferior:
				prom = 0
			elif prom >= umbSuperior:
				prom = 255
			newTupla = (prom,prom,prom)
			im.putpixel((x, y), newTupla)			

			#print tupla, "--", a,",",b,",",c
	im.save('meh5.jpg')
	#tiempoFinal = time.time()
	#transcurrido = tiempoFinal - tiempoInicial
	#print "Tiempo transcurrido durante la binarizacion = ", transcurrido


def salPimienta(): # Subrutina para poner sal y pimienta a la imagen binarizada
	#tiempoInicial = time.time()
	i = 0
	x = 0
	y = 0

	#Valores para instensidad y polarizacion respectivamente
	intensidad = int(argv[1]) # Nivel de pixeles (cantidades)
	polarizacion = int(argv[2]) # Que tan negros y blancos son los puntos en porcentaje... donde 0 es negro y 255 es blanco

	im = Image.open("mina.jpeg")
	pix = im.load()
	for x in range(im.size[0]):
		for y in range(im.size[1]):
			#pix = im.load()
			tupla = pix[x, y]
			azar = int(random.randint(0,intensidad))

			if azar == 9: #Aqui podria ser perfectamente cualquier numero (no necesariamente 9), seria la misma probabilidad: 1/intensidad
				if polarizacion > 25 and polarizacion < 75:	
					a = 128 + 64
					b = 128 + 64 	# Para puntos "blancos"
					c = 128 + 64

					# Fabricando la nueva tupla
					tupla1 = (a, b, c)
					
					# Poniendo pixel
					im.putpixel((x, y), tupla1)
				
				elif polarizacion >= 75:
					a = 255
					b = 255	# Para puntos "blancos"
					c = 255
					
					# Fabricando la nueva tupla
					tupla1 = (a, b, c)

					#Poniendo pixel
					im.putpixel((x, y), tupla1)

				elif polarizacion <= 25:
					a = 128 + 20
					b = 128 + 20	# Para puntos "blancos"
					c = 128 + 20
					
					# Fabricando la nueva tupla	
					tupla1 = (a, b, c)

					#Poniendo pixel
					im.putpixel((x, y), tupla1)
		
			elif azar == 7:
				if polarizacion > 25 and polarizacion < 75:	
					d = 128 - 64
					e = 128 - 64	# Para puntos "negros"
					f = 128 - 64
					tupla2 = (d, e, f)
					im.putpixel((x, y), tupla2)

				elif polarizacion >= 75:
					d = 0
					e = 0	# Para puntos "negros"
					f = 0
					tupla2 = (d, e, f)
					im.putpixel((x, y), tupla2)
				
				elif polarizacion <= 25:
					d = 128 - 20
					e = 128 - 20	# Para puntos "negros"
					f = 128 - 20
					tupla2 = (d, e, f)
					im.putpixel((x, y), tupla2)
					

			else:
				a = tupla[0]
				b = tupla[1]
				c = tupla[2]	
				
				newTupla = (a,b,c)
				im.putpixel((x, y), newTupla)			

			#print tupla, "--", a,",",b,",",c
	im.save('meh6.jpg')
	#tiempoFinal = time.time()
	#transcurso = tiempoFinal - tiempoInicial
	#print "Tiempo de escala de grises = ", transcurso 

def quitarSalPimienta():
	
	i = 0
	x = 0
	y = 0
	im = Image.open("meh6.jpg")
	pix = im.load() 
	width, height = im.size
	promedio = 0
	width = width-1
	height = height-1

	#x = j y y = i
	for x in range(height):
		for y in range(width):
			
			tupla = pix[y, x]
			pR = tupla[0]
			pG = tupla[1]
			pB = tupla[2]
		
			print(tupla)
			
			#if (pB == 0 or pR == 255):	
			if (pR >= 240 or pG >= 240 or pB >= 240) or (pR <=10 or pG <=10 or pB <=10):
				#esquina superior izquierda
				if y == 0 and x == 0:
					#promedio = (sum(pix[y + 1,x])/3 + sum(pix[y,x + 1])/3 + sum(pix[y,x])/3)/3
					promedio1 = (pix[y + 1,x][0] + pix[y,x + 1][0])/2
					promedio2 = (pix[y + 1,x][1] + pix[y,x + 1][1])/2
					promedio3 = (pix[y + 1,x][2] + pix[y,x + 1][2])/2
				#esquina superior derecha	
				if y == width and x == 0:
					#promedio = (sum(pix[y,x+1])/3 + sum(pix[y-1,x])/3 + sum(pix[y,x])/3)/3
					promedio1 = (pix[y,x+1][0] + pix[y-1,x][0])/2
					promedio2 = (pix[y,x+1][1] + pix[y-1,x][1])/2	
					promedio3 = (pix[y,x+1][2] + pix[y-1,x][2])/2

				if y == 0 and x == height:
						#promedio = (sum(pix[y,x-1])/3 + sum(pix[y+1,x])/3 + sum(pix[y,x])/3)/3
					promedio1 = (pix[y,x-1][0] + pix[y+1,x][0])/2
					promedio2 = (pix[y,x-1][1] + pix[y+1,x][1])/2
					promedio3 = (pix[y,x-1][2] + pix[y+1,x][2])/2

				if y == height and x == width:
						#promedio = (sum(pix[y - 1,x])/3 + sum(pix[y,x - 1])/3 + sum(pix[y,x])/3)/3
					promedio1 = (pix[y - 1,x][0] + pix[y,x - 1][0])/2
					promedio2 = (pix[y - 1,x][1] + pix[y,x - 1][1])/2
					promedio3 = (pix[y - 1,x][2] + pix[y,x - 1][2])/2


				if y > 0 and y < width and x == 0:
					#promedio = (sum(pix[y+1,x])/3 + sum(pix[y-1,x])/3 +sum(pix[y,x+1])/3+ sum(pix[y,x])/3)/4
					promedio1 = (pix[y+1,x][0] + pix[y-1,x][0] + pix[y,x+1][0])/3
					promedio2 = (pix[y+1,x][1] + pix[y-1,x][1] + pix[y,x+1][1])/3
					promedio3 = (pix[y+1,x][2] + pix[y-1,x][2] + pix[y,x+1][2])/3
		
				if y > 0 and y < width and x == height:
					#promedio = (sum(pix[y -1,x])/3 + sum(pix[y,x-1])/3 +sum(pix[y+1,x])/3+ sum(pix[y,x])/3)/4
					promedio1 = (pix[y -1,x][0] + pix[y,x-1][0] + pix[y+1,x][0])/3
					promedio2 = (pix[y -1,x][1] + pix[y,x-1][1] + pix[y+1,x][1])/3
					promedio3 = (pix[y -1,x][2] + pix[y,x-1][2] + pix[y+1,x][2])/3

				if x >0 and x <height and y == 0:
					#promedio = (sum(pix[y+1,x])/3 + sum(pix[y,x-1])/3 +sum(pix[y,x +1])/3+ sum(pix[y,x])/3)/4
					promedio1 = (pix[y+1,x][0] + pix[y,x-1][0] + pix[y,x +1][0])/3
					promedio2 = (pix[y+1,x][1] + pix[y,x-1][1] + pix[y,x +1][1])/3
					promedio3 = (pix[y+1,x][2] + pix[y,x-1][2] + pix[y,x +1][2])/3

				if y == width and x >0 and x < height:
					#promedio = (sum(pix[y - 1,x])/3 + sum(pix[y,x-1])/3 + sum(pix[y,x +1])/3+ sum(pix[y,x])/3)/4
					promedio1 = (pix[y - 1,x][0] + pix[y,x-1][0] + pix[y,x +1][0])/3
					promedio2 = (pix[y - 1,x][1] + pix[y,x-1][1] + pix[y,x +1][1])/3
					promedio3 = (pix[y - 1,x][2] + pix[y,x-1][2] + pix[y,x +1][2])/3

				if y > 0 and y< width and x>0 and x< height:
					#promedio = (sum(pix[y,x])/3 + sum(pix[y + 1,x])/3 + sum(pix[y - 1,x])/3 + sum(pix[y,x + 1])/3 + sum(pix[y,x -1])/3)/5	
					promedio1 = (pix[y + 1,x][0] + pix[y - 1,x][0] + pix[y,x + 1][0] + pix[y,x -1][0])/4
					promedio2 = (pix[y + 1,x][1] + pix[y - 1,x][1] + pix[y,x + 1][1] + pix[y,x -1][1])/4
					promedio3 = (pix[y + 1,x][2] + pix[y - 1,x][2] + pix[y,x + 1][2] + pix[y,x -1][2])/4
			#-----------------------------
			#tupla = pix[x, y]
			
				a = promedio1
				b = promedio2
				c = promedio3	
				miTupla = (a,b,c) #Eso no es una tupla, pero asi le digo yo :P
				im.putpixel((y, x), miTupla) #Esto si es una tupla
				#pix[y, x] = (a,b,c)
			
			else:	
				tuplaOriginal = (pR, pG, pB) #Esto tampoco es una tupla, pero asi le digo yo :P
				im.putpixel((y, x), tuplaOriginal) #Esto si es una tupla XD
			'''
			newTupla = (prom,prom,prom)
			im.putpixel((x, y), newTupla)	
			'''		

			#print tupla, "--", a,",",b,",",c
	im.save('meh7.jpg')

#Implelementacion de bfs ***************************************************
#***************************************************************************

def bfs(im, origen, color):
	n = 0	
	pixel = im.load()
	width, height = im.size
	col = []
	xsum = []
	ysum = []
	col.append(origen)
	original = pixel[origen]
	#largo = len(col)	
	
	while len(col) > 0:
								(x, y) = col.pop(0)
								actual = pixel[x, y]
								if actual == original or actual == color:
												for dx in [-1, 0, 1]:
																for dy in [-1, 0, 1]:
																				i, j = (x + dx, y + dy)
																				if i >= 0 and i < width and j >= 0 and j < height:
																								contenido = pixel[i, j]
																								if contenido == original:
																												pixel[i, j] = color
																				xsum.append(i)
																				ysum.append(j)
																				n += 1
																				col.append((i, j))
	#im.save('bla01.jpg')
	return n, xsum, ysum # el regreso para la funcion formas
	
#Para clasificar los objetos**********************************************
#*****************************************************************************
#*************************************************************************

def formas():

	im = Image.open("meh5.jpg") #Imagen con bordes y binarizada
	width, height = im.size
	total = width * height
	porcentajes = []
	centro = []
	corr = 0 ##Solo para corroborar porcentajes
	conteo = 0
	pixel = im.load()
	temp = []
	colorsR = [] #Para guardar colores R
	colorsG = [] #Para guardar colores G
	colorsB = [] #Para guardar colores B
	conteoColores = 0
	for i in range(width):			#Recorriendo imagen
				for j in range(height):		#Recorriendo imagen
							if pixel[i, j] == (0, 0, 0):	#Ir pintando pixeles (negros obviamente)
										r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)  #Asignando pixeles random
										n, x, y = bfs(im,(i,j),(r,g,b))
										ptemp = float(n)/float(total) * 100.0	#Obteniendo porcentajes
										if ptemp > 0.2:
													centro.append((sum(x) / len(x), sum(y) / len(y)))	  #Localizando centros
													porcentajes.append([ptemp, (r, g, b)])
													conteo += 1
										else:
													temp.append((x, y))
	fondo = porcentajes.index(max(porcentajes))
	color = porcentajes[fondo][1]
	for i in range(width):
						for j in range(height):
									if pixel[i, j] == color:
											pixel[i, j] = (150, 150, 150)
	
	for i in range(len(centro)):
				if i == fondo:
								pixel[centro[i]] = (255, 0, 0)	#Para poner centros de masa
	#Aqui va lo de las tags, proximamente en Tkinter o Pygame
				else:
							pixel[centro[i]] = (0, 0, 0)	

	im.save('bla02.jpg')	#Imagen definitiva
	conteo = 0
	for ptemp in porcentajes:
				print("Porcentaje de figura %s: %.2f"%(conteo, ptemp[0]))
				conteo = conteo+ 1
	corr = ptemp[0] + corr 
	#print "Corroborando porcentaje: ", corr

# FIN ********************************************************************

'''

es un resumen sobre tecnicas para estudio de campo que permiten evaluar a nivel conceptual proyectos de computo ubicuo

'''


if __name__ == "__main__":
	main()






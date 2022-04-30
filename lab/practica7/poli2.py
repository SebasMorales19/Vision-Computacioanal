#!/usr/bin/python
#from Tkinter import *
from PIL import Image, ImageTk
import math
import sys
import filtros
import random
import ImageFont, ImageDraw
import Image
from math import sqrt, atan2, pi, atan
from collections import defaultdict


#file = argv[1]

#im = Image.open(file).convert("RGB")
#original = im
#(x,y) = im.size

def b_and_w(scale):
    grayscale("prom")
    for i in range(x):
        for j in range(y):
            pixel = im.getpixel((i,j))[0]
            if(pixel<scale):
                pixel = 0
            else:
                pixel = 255
            im.putpixel((i,j), (pixel,pixel,pixel))

def grayscale(tipo):
    for i in range(x):
        for j in range(y):
            (r,g,b)=original.getpixel((i, j))
            if tipo == "min":
                gray = min((r,g,b))
            if tipo == "max":
                gray = max((r,g,b))
            if tipo == "r":
                gray = r
            if tipo == "g":
                gray = g
            if tipo == "b":
                gray = b
            if tipo == "prom":
                gray = (r+g+b)/3
            im.putpixel((i,j), (gray,gray,gray))

def blur(maxiter, normalizado):
    grayscale("prom")
    iter = 0
    while iter < maxiter:
        print("Iteracion: ", iter)
        for i in range(x):
            for j in range(y):
                prom = []
                k=0
                pixel=im.getpixel((i, j))[0]
                if(i-1>=0):
                    prom.append(im.getpixel((i-1, j))[0])
                    k+=1
                if(i+1<x):
                    prom.append(im.getpixel((i+1, j))[0])
                    k+=1
                if(j+1<y):
                    prom.append(im.getpixel((i, j+1))[0])
                    k+=1
                if(j-1>=0):
                    prom.append(im.getpixel((i, j-1))[0])
                    k+=1
                promedio = 0;
                for valor in prom:
                    promedio+=valor
                promedio=promedio/k
                im.putpixel((i,j), (promedio,promedio,promedio))            
        iter+=1

def color_blur(maxiter):
    iter = 0
    while iter < maxiter:
        for i in range(x):
            for j in range(y):
                promr = []
                promg = []
                promb = []
                k=0
                (r,g,b)=original.getpixel((i, j))
                if(i-1>=0):
                    (rn,gn,bn)=original.getpixel((i-1, j))
                    promr.append(rn)
                    promg.append(gn)
                    promb.append(bn)
                    k+=1
                if(i+1<x):
                    (rs,gs,bs)=original.getpixel((i+1, j))
                    promr.append(rs)
                    promg.append(gs)
                    promb.append(bs)
                    k+=1
                if(j+1<y):
                    (re,ge,be)=original.getpixel((i, j+1))
                    promr.append(re)
                    promg.append(ge)
                    promb.append(be)
                    k+=1
                if(j-1>=0):
                    (ro,go,bo)=original.getpixel((i, j-1))
                    promr.append(ro)
                    promg.append(go)
                    promb.append(bo)
                    k+=1
                promedior = 0
                promediog = 0
                promediob = 0
                for valor in promr:
                    promedior+=valor
                for valor in promg:
                    promediog+=valor
                for valor in promb:
                    promediob+=valor
                promedior=promedior/k
                promediog=promediog/k
                promediob=promediob/k
                im.putpixel((i,j), (promedior,promediog,promediob))
        iter+=1

def getcolor(color):
    for i in range(x):
        for j in range(y):
            (r,g,b)=original.getpixel((i,j))
            if(color=="r" or color=="R"):
                im.putpixel((i,j),(r,0,0))
            if(color=="g" or color =="G"):
                im.putpixel((i,j),(0,g,0))
            if(color=="b" or color == "B"):
                im.putpixel((i,j),(0,0,b))

def color_inv():
    for i in range(x):
        for j in range(y):
            (r,g,b)=original.getpixel((i,j))
            im.putpixel((i,j),(255-r,255-g,255-b))

    if(argv[2]=="INV" or argv[2]=="inv"):
        color_inv()
        im.save("INV_"+file)
        
        if(argv[2]=="GC" or argv[2]=="gc"):
            if(len(argv)==4):
                getcolor(argv[3])
                im.save("GC_"+file)
            else:
                print("Introduzca 'r', 'g' o 'b' segun el color que desee extraer.")

                if(argv[2]=="BW" or argv[2]=="bw"):
                    if(len(argv)==4):
                        b_and_w(int(argv[3]))
                        im.save("BW_"+file)
                    else:
                        print("Introduzca la escala de blanco y negro como parametro.")
        
                        if(argv[2]=="G" or argv[2]=="g"):
                            if(len(argv)==4):
                                grayscale(argv[3])
                                im.save("G_"+file)
                            else:
                                print("Introduzca el tipo de escala de gris (min, max, r, g, b, prom).")
        
                                if(argv[2]=="B" or argv[2]=="b"):
                                    if(len(argv)==4):
                                        blur(int(argv[3]), False)
                                        im.save("B_"+file)
                                    else:
                                        print("Introduzca el numero de iteraciones de blur como parametro.")
        
                                        if(argv[2]=="CB" or argv[2]=="cb"):
                                            if(len(argv)==4):
                                                color_blur(int(argv[3]))
                                                im.save("CB_"+file)
                                            else:
                                                print("Introduzca el numero de iteraciones de blur como parametro.")




DEBUG = True
#DEBUG = False

def gradiente_sobel(punto, imagen):
    #print punto
    pixeles = imagen.load()
    x = punto[0]
    y = punto[1]
    #print x, y
    z1 = pixeles[x-1, y-1][0] 
    z2 = pixeles[x, y-1][0]
    z3 = pixeles[x+1, y-1][0]
    z4 = pixeles[x-1, y][0]
    z5 = pixeles[x, y][0]
    z6 = pixeles[x+1, y][0]
    z7 = pixeles[x-1, y+1][0]
    z8 = pixeles[x, y+1][0]
    z9 = pixeles[x+1, y+1][0]
    Gx = ((z3)+(2*z6)+z9)-((z1)+(2*z4)+(z7))
    Gy = ((z7)+(2*z8)+z9)-((z1)+(2*z2)+(z3))
    G = sqrt((Gx**2)+(Gy**2))
    angulo = atan2(Gy, Gx)
    angulo = angulo -(pi/2)
    angulo = float("%.4f" % angulo)
    return x,y, angulo 


def bfs(imagen, origen, color):
    """colorea todo el objeto recibe como parametros el 
    nuevo color con el que se pinta,la coordenada de inicio y
    la imagen, y regresa un arreglo con la masa y la imagen
    """
    c = []
    cola = []
    cont = 0
    masa = []
    pixeles = imagen.load()
    alto, ancho = imagen.size
    cola.append(origen)
    original = pixeles[origen]
    edges = []
    while len(cola) > 0:
        (x, y) = cola.pop(0)
        actual = pixeles[x, y]
        if actual == original or actual == color:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    candidato = (x + dx, y + dy)
                    pix_x = candidato[0]
                    pix_y = candidato[1]
                    if pix_x >= 0 and pix_x < alto and pix_y >= 0 and pix_y < ancho:
                        contenido = pixeles[pix_x, pix_y]
                        if contenido == original:
                            pixeles[pix_x, pix_y] = color
                            masa.append((pix_x,pix_y))
                            imagen.putpixel((pix_x, pix_y), color)
                            cont += 1
                            cola.append((pix_x, pix_y))
                            c.append((pix_x, pix_y))
    imagen.save('prueba', 'png')
    return imagen, cont, masa, c


def encuentra_figuras(imagen):
    """encuentra cada objeto y guarda en una lista
    los bordes de cada objeto
    """
    alto, ancho = imagen.size
    pixeles = imagen.load()
    colores = []
    cen = []
    porcentaje = []
    contornos = []
    for i in range(alto):
        for j in range(ancho):
            if pixeles[i,j] == (255,255,255):
                r = int(random.random()*250)
                g = int(random.random()*250)
                b = int(random.random()*250)
                nuevo_color = (r,g,b)
                imagen, cont, masa, c = bfs(imagen, (i,j), nuevo_color)
                contornos.append(c)
                total_x = 0
                total_y = 0
                por = (float(cont)/float(alto*ancho))*100
                for l in range(len(masa)):
                    total_x = total_x + masa[l][0]
                    total_y = total_y + masa[l][1]
                x_centro = total_x/len(masa)
                y_centro = total_y/len(masa)
                cen.append((x_centro, y_centro))
                #draw.ellipse((x_centro+1, y_centro+1, x_centro-1, y_centro-1), fill=(255,0,255))
                colores.append([nuevo_color,(x_centro, y_centro), por])
                porcentaje.append(por)
                pixeles = imagen.load()
                masa = []
    #figura_mayor = max(porcentaje)
    #i = porcentaje.index(figura_mayor)
    #color_mayor = colores[i][0]
    imagen.save('colores.png', 'png')
    #aux.save('poligonos.png', 'png')
    return contornos, cen

def main():
    """funcion principal
    """
    try:
        imagen_path = sys.argv[1]
        print("Imagen seleccionada %s" %imagen_path)
        imagen = filtros.abrir_imagen(imagen_path)
        
    except:
        print("No seleccionaste una imagen")
        return
    imagen = filtros.hacer_gris(imagen)
    mascara = [[0,1,0],[1,-4,1],[0,1,0]]
    imagen = filtros.convolucion(imagen, mascara)
    imagen = filtros.umbral(imagen)

    contornos, cen = encuentra_figuras(imagen.copy())
    if DEBUG:
        print("Figuras encontradas %s" %len(contornos))
    else:
        pass
    listas = []
    nueva = imagen.copy()
    todos = nueva.load()
    for i in contornos:
        dic = defaultdict(list)
        for punto in i:
            x,y,angulo= gradiente_sobel(punto, imagen)
            dic[angulo].append((x,y))
        listas.append(dic)
    for i in listas:
        print("*************************************")
        for j in i:
            r = int(random.random()*250)
            g = int(random.random()*250)
            b = int(random.random()*250)
            color = (r,g,b)
            print(j)
            print(color)
            for k in i[j]:
                print(k)
                nueva.putpixel((k[0], k[1]), color)
    nueva.save("ss.png")
    f=open("centros.txt","w")
    for i in cen:
        f.write('%s,%s\n' %(i[0], i[1]))
    f.close

if __name__ == "__main__":
    main()

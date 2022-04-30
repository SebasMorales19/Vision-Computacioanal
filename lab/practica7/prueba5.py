#import cv
from PIL import Image
import numpy as np
import math
from math import *
from sys import argv
import random

def detect_painting(image):
    im=Image.open(image)
    #img=image.copy()
    imagen = filtro(image)
    img,gx,gy,minimo,maximo,conv = mascara(imagen)
    masa,imagen=formas(image)
    print('img',img)
    input()
    print('termino formas')
    obtener_lineas(masa,imagen,gx,gy)

def formas(img):
    imagen,masa=c_colorear(img)
    return masa,imagen

def obtener_lineas(poligonos,imagen,gx,gy):
    poligonos.pop(0)
    rectangulos=[]
    for poligono in poligonos:
        pendientes,med=get_pendientes(poligono,imagen,gx,gy)
        print('regreso de obtener pendientes')
        imagen,segmentos=get_rectas(pendientes,imagen,poligono,med)
        num=len(segmentos)

def get_rectas(pendientes,img,poligono,med):
    segmentos=list()
    pixels=img.load()
    ancho,alto=img.size
    for m in med:
        linea=[]
        r,g,b= random.randint(0,255),random.randint(0,255), random.randint(0,255)
        fondo=(r,g,b)
        for p in poligono:
            i,j=p
            if pendientes[i,j]==m:
                pixels[i,j]=fondo
                linea.append((i,j))
            if len(linea)>15:
                segmentos.append(linea)
    img.save('i.png')
    return img,segmentos
    
def get_pendientes(puntos,imagen,gx,gy):
    Gx=gx
    Gy=gy
    pixels=imagen.load()
    ancho,alto=imagen.size
    pendientes=np.empty((ancho, alto))
    med=[]
    for p in puntos:
        i,j=p
        if Gx[i,j]<0 and Gy[i,j]>0:
                m=0
        elif Gx[i,j]>0 and Gy[i,j]<0:
            m=1
        elif Gy[i,j]<=0 and Gx[i,j]==0:
            m=2
        elif Gy[i,j]>=0 and Gx[i,j]==0:
            m=3
        elif Gx[i,j]<=0 and Gy[i,j]==0:
            m=4
        elif Gx[i,j]>=0 and Gy[i,j]==0:
                m=5
        elif Gx[i,j]<0 and Gy[i,j]<0:
            m=6
        elif Gy[i,j]>0 and Gx[i,j]>0:
            m=7
        if m not in med:
            med.append(m)
        pendientes[i,j]=m

    print('termino')
    print('pendientes',pendientes)
    return pendientes,med

def boton_convolucion(img):
    image = filtro(img)
    ima=image.save('filtrada2.jpg')
    image,gx,gy,minimo,maximo,conv = mascara(image)
    id = image.save('mascara.png')
    img=normalizar(image,minimo,maximo,conv)
    img2 = img.save('normalizada.png')
    im_bin = binarizar(img)
    imbin=img.save('binarizada.png')
    return im_bin

def c_colorear(img):
    img=boton_convolucion(img)
    pixels=img.load()
    porcentajes=[]
    fondos=[]
    centro_masa=[]
    masa=[]
    ancho,alto=img.size
    t_pixels=ancho*alto
    c=0
    pintar=[]
    f=0
    m=[]
    for i in range(ancho):
        for j in range(alto):
            pix = pixels[i,j]
            r,g,b= random.randint(0,255),random.randint(0,255), random.randint(0,255)
            fondo=(r,g,b)
            if (pix==(255,255,255)):
                print('entro')
                c +=1
                origen=(i,j)
                num_pixels,abscisa,ordenada,puntos=bfs(pix,origen,img,fondo)
                p=(num_pixels/float(t_pixels))*100
                if p>.10:
                    centro=(sum(abscisa)/float(num_pixels),sum(ordenada)/float(num_pixels))
                    centro_masa.append(centro)
                    masa.append(num_pixels)
                    porcentajes.append(p)
                    fondos.append(fondo)
                    m.append(puntos)
                    centro_masa.append(centro)
    img.save('final.jpg')
    return img,m

def centro_masa(im,centros):
    draw = ImageDraw.Draw(im)
    for i,punto in enumerate(centros):
        draw.ellipse((punto[0]-2, punto[1]-2, punto[0]+2, punto[1]+2), fill=(0,0,0))
        label_id = Label(text=i)
        label_id.place(x = punto[0]+16,  y = punto[1])
    im.save('centro.png')
    return
 
def imprimir_porcentajes(porcentajes):
    for i,p in enumerate(porcentajes):
        print('Figura ID: %d  Porcentaje: %f' %(i,p))
        

def bfs(pix,origen,im,fondo):
    pixels=im.load()
    cola=list()
    lista=[-1,0,1]
    abscisa=[]
    ordenada=[]
    puntos=[]
    cola.append(origen)
    original = pixels[origen]
    num=1
    while len(cola) > 0:
        (i,j)=cola.pop(0)
        actual = pixels[i,j]
        if actual == original or actual==fondo:
            for x in lista:
                for y in lista:
                    a= i+x
                    b = j+y 
                    try:
                        if pixels[a,b]:
                            contenido = pixels[a,b]
                            if contenido == original:
                                pixels[a,b] = fondo
                                abscisa.append(a)
                                ordenada.append(b)
                                num +=1
                                cola.append((a,b))
                                puntos.append((a,b))
                    except IndexError:
                        pass
    im.save('FORMAS.png')
    return num,abscisa,ordenada,puntos
    

def mascara(image):
    sobelx = ([-1,0,1],[-2,0,2],[-1,0,1]) #gradiente horizontal
    sobely = ([1,2,1],[0,0,0],[-1,-2,-1]) # gradiente vertical    
    img,gx,gy,minimo,maximo,conv=convolucion(sobelx,sobely,image)
    return img,gx,gy,minimo,maximo,conv
  
def convolucion(h1,h2,image):
    pixels = image.load()
    ancho,alto = image.size 
    a=len(h1[0])
    conv = np.empty((ancho, alto))
    gx=np.empty((ancho, alto))
    gy=np.empty((ancho, alto))
    minimo = 255
    maximo = 0
    for x in range(ancho):
        for y in range(alto):
            sumax = 0.0
            sumay = 0.0
            for i in range(a): 
                for j in range(a): 
                    try:
                        sumax +=(pixels[x+i,y+j][0]*h1[i][j])
                        sumay +=(pixels[x+i,y+j][0]*h2[i][j])

                    except:
                        pass
            gradiente = math.sqrt(pow(sumax,2)+pow(sumay,2))
            conv[x,y]=gradiente
            gx[x,y]=sumax
            gy[x,y]=sumay
            gradiente = int(gradiente)
            pixels[x,y] = (gradiente,gradiente,gradiente)
            p = gradiente
            if p <minimo:
                minimo = p
            if  p > maximo:
                maximo = p
    image.save('MASCARA.png')
    return image,gx,gy,minimo,maximo,conv

def normalizar(image,minimo,maximo,conv):
    #inicio=time()
    pixels = image.load()
    r = maximo-minimo
    prop = 255.0/r
    ancho,alto = image.size
    for i in range(ancho):
        for j in range(alto):
            p =int(floor((conv[i,j]-minimo)*prop))
            pixels[i,j]=(p,p,p);
        # print 'TERMINO'
        # print "Tiempo que tardo en ejecutarse normalizar = "+str(tiempo_t)+" segundos"
    return image


def binarizar(img):
   # inicio = time()
    pixels = img.load()
    ancho,alto = img.size
    minimo = int(argv[2])
    for i in range(ancho):
        for j in range(alto):
            if pixels[i,j][1] < minimo:
                p=0
            else:
                p= 255
            pixels[i,j]=(p,p,p)
       # print "Tiempo que tardo en ejecutarse binzarizar = "+str(tiempo_t)+" segundos"

    return img

def filtro(image):
    image,matriz = escala_grises(image)
    pixels = image.load()
    ancho, alto =image.size
    lista = [-1,0,1]
    for i in range(ancho):
        for j in range(alto):
            promedio = vecindad(i,j,lista,matriz)
            pixels[i,j] = (promedio,promedio,promedio)
    image.save('FILTRO.png')
    return image

def escala_grises(image):
    image = Image.open(image) 
    pixels = image.load()
    ancho,alto = image.size
    matriz = np.empty((ancho, alto))
    for i in range(ancho):
        for j in range(alto):
            (r,g,b) = image.getpixel((i,j))
            escala= int((r+g+b)/3)
            pixels[i,j] = (escala,escala,escala)
            matriz[i,j] = int(escala)
    df = image.save('escala.png')
    return image,matriz 

    
def vecindad(i,j,lista,matriz):
    promedio = 0
    indice  = 0
    for x in lista:
        for y in lista:
            a = i+x
            b = j+y
            try:
                if matriz[a,b] and (x!=a and y!=b):
                    promedio += matriz[a,b] 
                    indice +=1            
            except IndexError:
                pass
            try:
                promedio=int(promedio/indice)
                return promedio
            except ZeroDivisionError:
                return 0  

def main():
    detect_painting("mina.jpeg")
main()

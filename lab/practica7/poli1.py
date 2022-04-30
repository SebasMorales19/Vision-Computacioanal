#import cv
from PIL import Image,ImageDraw
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
    masa,imagen,centros=formas(image)
    print('img',img)
    #checar_pintura(rectangulos,image)
    #detect_rectangulo(masa,imagen,centros)
    #raw_input()
    print('termino formas')

#def checar_pintura(rectangulos,image):
#    im='test.png'
#    lr=[]
#    lg=[]
#    lb=[]
#    print('im',im)
#    im=Image.open(im)
#    pixels=im.load()
#    for rec in rectangulos:
#        for x,y in rec:
#            lr.append(lr)
#            lg.append(lg)
#            lb.append(lb)

#    minimor = min(lr)
#    maximor = max(lr)
#    minimog = min(lg)
#    maximog = max(lg)
#    minimob = min(lb)
#    maximob = max(lb)
#    print 'termino calcular rgb'
#    if minimor<54 and minimog<94 and minimob<97:
#        print 'CORRECTO'
 
def formas(img):
    #imagen,masa,centros,rectangulos=c_colorear(img)
    imagen, masa,centros = c_colorear(img)
    return masa,imagen,centros

#def draw_recta(im,puntos, color,base,altura):
#    draw = ImageDraw.Draw(im)
#    x,y=max(puntos)
#    print 'x,y',x,y
#    im.save('CHECAR.png')
#    print 'base,altura',base,altura
   # draw.rectangle(((x, y), (base,altura)), alpha,2)
        

#def detectar_rectangulo(num_pixeles,im,centro,puntos,fondo):
#    ima=im.load()
#    rect=[]
#    area,base,altura=search(num_pixeles,im,centro,puntos,fondo)
#    if  num_pixeles<area<num_pixeles+4000:
#        #print 'RECTANGULO'
#        for i,j in puntos:
#            ima[i,j]=(255,0,0)
        #draw_recta(im,puntos,(0,0,255),base,altura)
#    im.save('rectangulo.png')
   # raw_input(
#    return puntos

def search(num_pixeles,imagen,centro,puntos,fondo):
    pixels=imagen.load()
    inicio=centro
    x,y=int(centro[0]),int(centro[1])
    base_1=2*(base(x,y,pixels,imagen,fondo))
    altura_1=2*(altura(x,y,pixels,imagen,fondo))
    print('base', base_1)
    print('altura',altura_1)
    area=base_1*altura_1
    return area,base_1,altura_1

#def base(aumenta,igual,pixels,im,fondo):
#    print 'sacando base'
#    pixels=im.load()
#    a=0
#    while True:
#        if (pixels[aumenta,igual]==fondo):
#            aumenta +=1
#            a +=1 
#        else:
#            break
#    return a


#def altura(igual,aumenta,pixels,im,fondo):
#    print 'sacando altura'
#    pixels=im.load()
#    b=0 
#    while True:
#        if (pixels[igual,aumenta]==fondo):
#            aumenta +=1
#            b +=1                                                                                            
#        else:
#            break
#    return b


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
    rect=[]
    f=0
    rec=[]
    m=[]
    for i in range(ancho):
        for j in range(alto):
            pix = pixels[i,j]
            r,g,b= random.randint(0,255),random.randint(0,255), random.randint(0,255)
            fondo=(r,g,b)
            if (pix==(0,0,0)):
                #print 'entro'
                c +=1
                origen=(i,j)
                num_pixels,abscisa,ordenada,puntos=bfs(pix,origen,img,fondo)
                p=(num_pixels/float(t_pixels))*100
                if p>.3:
                    centro=(sum(abscisa)/float(num_pixels),sum(ordenada)/float(num_pixels))
                    centro_masa.append(centro)
                    masa.append(num_pixels)
                    porcentajes.append(p)
                    fondos.append(fondo)
                    m.append(puntos)
                    #rect.append(puntos)
                    centro_masa.append(centro)
                    #p_r=detectar_rectangulo(num_pixels,img,centro,puntos,fondo)
                    #rec.append(p_r)
    img.save('final.jpg')
    return img,m,centro_masa

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
        # print('TERMINO')
        # print("Tiempo que tardo en ejecutarse normalizar = "+str(tiempo_t)+" segundos")
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
       # print("Tiempo que tardo en ejecutarse binzarizar = "+str(tiempo_t)+" segundos")

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
    #cam=cv.CaptureFromCAM(0)
    detect_painting("mina.jpeg")
    #while True:
        #im =cv.QueryFrame(cam)
        #snapshot = im
        #image_size = cv.GetSize(snapshot)
        #cv.SaveImage("test.png",im)
        #imagen=cv.CreateImage(image_size,cv.IPL_DEPTH_8U,3)
        
        #cv.ShowImage('Camara', snapshot)
        #if cv.WaitKey(30)==27:
        #    break

main()
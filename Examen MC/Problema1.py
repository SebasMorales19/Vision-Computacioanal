  
import numpy as np
import cv2 as cv
import math
import grey_conversion as grey_cv
import utils
import umbral

def variance_based(image, flattened, k, N, sorted_img):
  # ni how many times each element is repeated
  n_i = []
  # pi probability of appearing in the image
  p_i = []
  for value in sorted_img:
    appeareance_in_image = np.count_nonzero( flattened == value )
    n_i.append(appeareance_in_image)
    p_i.append( appeareance_in_image/N)
  n_i = np.array(n_i)
  p_i = np.array(p_i)
  PI0 = sum(p_i[0:k])
  PI1 = 1 - PI0

  aux_vector = [ 1 if i < k else 0 for i in range(0,N) ]
  # mu es la media aparente de esa sección
  mu0 = 0
  mu1 = 0
  # mu T es la media total
  muT = 0
  for i,value in enumerate(sorted_img):
    mu0 += (value*p_i[i]*aux_vector[i]/PI0)
    mu1 += (value*p_i[i]*(1-aux_vector[i])/PI1)
    muT += (value*p_i[i])
  varianceB = PI0*math.pow((mu0-muT),2) + PI1*math.pow((mu1-muT),2)
  varianceT = 0
  for i,value in enumerate(sorted_img):
    varianceT += ( math.pow((value-muT),2)*p_i[i] )
  eta = varianceB/varianceT

  return eta

"""
"""
def main():
  img = cv.imread("mina_cortada.png")
  grey_img = grey_cv.convert_to_greyscale(img)
  width = img.shape[1]
  height = img.shape[0]
  print("Elige el espacio de la imagen a cortar")
  a,b,c,d = utils.choose_image_section(width, height)
  cut_img = grey_img[c:d,a:b]
  # k is the alpha cut value
  #cut_img = [[127,122,177,189],[85,73,127,139],[75,61,102,128],[58,40,84,108]]
  cut_img = np.array(cut_img)
  flattened = cut_img.flatten()
  sorted_img = np.unique(flattened)
  N = len(flattened)
  umbral_values = []
  for i in range(1,len(sorted_img)):
    eta_value = variance_based(cut_img,flattened,i,N,sorted_img)
    umbral_values.append(eta_value)
  best_eta_idx = np.where( umbral_values == min(umbral_values))[0][0]
  best_umbral = sorted_img[best_eta_idx]
  print(umbral_values)
  print(best_umbral)
  #Retorna el mejor umbral y llama a función de umbral con este valor
  umbral_img = umbral.umbral_selection(cut_img, best_umbral)
  cv.imwrite("mina_umbral_variance.png",umbral_img)

if __name__ == '__main__':
  main()
import numpy as np
import cv2
import os


def takeImg(filename):
  """ Take image from the designated file """
  CurPath = os.path.dirname(__file__)
  inImg  = cv2.imread(CurPath + "/image/" + filename)
  return inImg

def crop_in_middle(Img, H, L):
  """ Return an image with the size is multiple size of (HxL) in the middle of original image"""
  M, N, G = Img.shape
  Hcrop = H*(M//H)
  Lcrop = L*(N//L)
  crop = Img[(H-Hcrop)//2:(H+Hcrop)//2][(L-Lcrop)//2:(L+Lcrop)//2][:]
  return crop


def convert_img_size(Img, H, L):
  """ Change current image size into designated size (HxL)"""
  M, N, G = Img.shape
  Hd, Hm = M // H, M % H
  Ld, Lm = N // L, N % L
  Resize = np.empty([H, L, 3])
  Resize1 = np.empty([M, L, 3])
  for g in range(3):
    for k in range(M):
      for i in range(Lm):
        sum = 0
        for j in range(Ld + 1):
          sum += Img[k][i * (Ld + 1) + j][g]
        Resize1[k][i][g] = sum / (Ld + 1)
      for i in range(Lm, L):
        sum = 0
        for j in range(Ld):
          sum += Img[k][Lm * (Ld + 1) + (i - Lm) * Ld + j][g]
        Resize1[k][i][g] = sum / (Ld)
  for g in range(3):
    for k in range(L):
      for i in range(Hm):
        sum = 0
        for j in range(Hd + 1):
          sum += Resize1[i * (Hd + 1) + j][k][g]
        Resize[i][k][g] = sum / (Hd + 1)

      for i in range(Hm, H):
        sum = 0
        for j in range(Hd):
          sum += Resize1[Hm * (Hd + 1) + (i - Hm) * Hd + j][k][g]
        Resize[i][k][g] = sum / (Hd)
  return Resize


def convert_color_form(Resize):
  M, N, G = Resize.shape
  ImgC = []
  for i in range(M):
    ImgC.append([])
    for j in range(N):
      ImgC[i].append((int(Resize[i][j][2]),int(Resize[i][j][1]), int(Resize[i][j][0])))
  return ImgC


def getImgColor(filename, H, L):
    Img = takeImg(filename)
    #ImgC = crop_in_middle(Img, H ,L)
    ResizedImg = convert_img_size(Img, H, L)
    ImgCl = convert_color_form(ResizedImg)
    return ImgCl


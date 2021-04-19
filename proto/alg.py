import cv2
import matplotlib
import numpy as np
import os
from PIL import Image
from matplotlib import pyplot as plt
if __name__ == "__main__":

    treshold=0
    cwd=os.getcwd()

    img=cv2.imread('eg/0.jpg',0)

    blur=cv2.GaussianBlur(img,(5,5),0)
    ret,th,=cv2.threshold(blur,treshold,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    plt.subplot(2,1,1),plt.imshow(th,'gray')
    plt.subplot(2,1,2),plt.imshow(img,'gray')
    plt.show()
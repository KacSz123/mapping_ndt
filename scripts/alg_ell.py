# import matplotlib
# import numpy as np
# import matplotlib.pyplot as plt
import PIL.Image
# from scipy.stats import multivariate_normal

from matplotlib.patches import Ellipse
import copy
from mymath import *
def EllipseOutOfSize(ell,epsilon):
    if ell.height > epsilon or ell.width>epsilon:
      return True
    else:
      return False


def GetListsOfEllipses(cell_s, img_name):
    cell_size = cell_s
    #img_name = 'img/123.bmp'

    im = PIL.Image.open(img_name, 'r')
    width, height = im.size
    pixel_values = list(im.getdata())

    cells_horizontal = width//cell_size
    cells_vertical = height//cell_size

    print('Dim: x=%d, y=%d, pixells:%d' % (width, height, width*height))
    print('Dim cell:x=%d Cells no. y=%d' % (cell_size, cells_horizontal*cells_vertical))

    x=[]
    y=[]
    for i in range(height*width):
        if (pixel_values[i]==0):
            x.insert(0,i%width)
            y.insert(0, height - i//height)
    current_x = []
    current_y = []     
    counter = 0     
    j=0
    ellsRL=[]  
    ells2P=[]
    ellsOrin=[]    
    for i in range(cells_vertical):
        for j in range(cells_horizontal):
            counter = 0  
            for k in range(cell_size):
                for l in range(cell_size):
                    if(pixel_values[(i*cell_size+k)*width + j*cell_size+l] == 0):
                        counter = counter +1
                        current_x.append((j*cell_size)+l)
                        current_y.append((height-(i*cell_size+k)))
            if(counter>3):
                ymi,ysigma = GetMuSigmaFromEqSqrt(current_y)
                if(ysigma<0.0001):
                     ysigma = 0.1
                xmi,xsigma = GetMuSigmaFromEqSqrt(current_x)
                if(xsigma<0.0001):
                     xsigma = 0.1

                ang2P=GetBeginEnd(current_x,current_y)
                angRL=RegLinp(current_x,current_y,xmi,ymi)
                ellsRL.append( Ellipse(xy=(xmi, ymi), width=2*xsigma, height=2*ysigma,angle=angRL,
                                     edgecolor='b', fc='None', lw=1))
                ells2P.append( Ellipse(xy=(xmi, ymi), width=2*xsigma, height=2*ysigma,angle=ang2P,
                                     edgecolor='b', fc='None', lw=1))
                
            current_x.clear()
            current_y.clear()
    return ells2P, ellsRL,width,height


def GetEllipsesFromCsv(cell_s, xy):
    
    current_x = []
    current_y = []     
    counter = 0     
    ellsRL=[] 
    i = 1
    while i<len(xy)-2:
        counter = 0
        for j in range(0, cell_s):
            if   i<len(xy)-1 and Dist2Points(xy[i],xy[i-1]) > 0.15:
                break
            elif i<len(xy)-1:
                current_x.append(xy[i][0])
                current_y.append(xy[i][1])
                counter+=1
            i+=1
        if i >=len(xy)-1:
            break
        if counter>2:
                ymi,ysigma = GetMuSigmaFromEqSqrt(current_y)
                if(ysigma<0.0001):
                     ysigma = 0.1
                xmi,xsigma = GetMuSigmaFromEqSqrt(current_x)
                if(xsigma<0.0001):
                     xsigma = 0.1
                angRL=RegLinp(current_x,current_y,xmi,ymi)
                if 4*xsigma<0.40 and 4*ysigma<0.40:
                    ellsRL.append( Ellipse(xy=(xmi, ymi), width=4*xsigma, height=4*ysigma,angle=angRL,
                                     edgecolor='b', fc='None', lw=1))
        current_x.clear()
        current_y.clear()    
        i+=1
    #print(len(ellsRL))
    return ellsRL     
def GetEllipsesFromScan(cells_no, x,y):
    print(1)
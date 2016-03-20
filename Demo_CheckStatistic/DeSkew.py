'''
Created on Mar 1, 2016

@author: JuniorK
'''
import cv2
import numpy as np
from cv2 import CV_LOAD_IMAGE_GRAYSCALE
from math import atan, pi, ceil
def compute_skew(image):
    #image = cv2.bitwise_not(image)
    height, width = image.shape[:2]
    edges = cv2.Canny(image, 150, 200, 3, 5)
    lines = cv2.HoughLinesP(edges, 1, cv2.cv.CV_PI/180, 100, minLineLength=width / 2.0, maxLineGap=20)
    angle = 0.0
    nlines = lines.size
    for x1, y1, x2, y2 in lines[0]:
        angle += np.arctan2(y2 - y1,x2 - x1)
        #cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
        print np.arctan2(y2 - y1,x2 - x1)
    cv2.imshow("",edges)
    cv2.waitKey(0)
    return angle / nlines

def deskew(image, angle):
    print angle
    image = cv2.bitwise_not(image)
    non_zero_pixels = cv2.findNonZero(image)
    center, wh, theta = cv2.minAreaRect(non_zero_pixels)

    root_mat = cv2.getRotationMatrix2D(center, angle, 1)
    rows,cols = image.shape[:2]
    rotated = cv2.warpAffine(image, root_mat, (cols, rows), flags=cv2.INTER_CUBIC)
    return cv2.bitwise_not(cv2.getRectSubPix(rotated, (cols, rows), center))
def deskew_base_hough(img):
    return deskew(img, compute_skew(img))
def deskew_base_moment(img):
    tmp=img
    h,w = img.shape[:2]
    m = cv2.moments(tmp)
    x = m['m10']/m['m00']
    y = m['m01']/m['m00']
    mu02 = m['mu02']
    mu20 = m['mu20']
    mu11 = m['mu11']
     
    lambda1 = 0.5*( mu20 + mu02 ) + 0.5*( mu20**2 + mu02**2 - 2*mu20*mu02 + 4*mu11**2 )**0.5
    lambda2 = 0.5*( mu20 + mu02 ) - 0.5*( mu20**2 + mu02**2 - 2*mu20*mu02 + 4*mu11**2 )**0.5 
    lambda_m = max(lambda1, lambda2)
     
    # Convert from radians to degrees
    angle =  ceil(atan((lambda_m - mu20)/mu11)*18000/pi)/100
    if angle>0:
        angle= min(angle,90-angle)
    else:
        angle= -1*min(-1*angle,90+angle) -0.1
    #print angle
     
    # Create a rotation matrix and use it to de-skew the image.
    center = tuple(map(int, (x, y)))
    rotmat = cv2.getRotationMatrix2D(center, angle , 1)
    rotatedImg = cv2.warpAffine(img, rotmat, (w, h), flags = cv2.INTER_CUBIC)     
    return rotatedImg  
#img=cv2.imread('test01.png',0)
#deskew_base_hough(cv2.pyrDown(img))



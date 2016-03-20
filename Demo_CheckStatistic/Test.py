'''
Created on Mar 14, 2016

@author: JunioK
'''
import cv2
import numpy as np
from wand.image import Image
with Image(filename='a.pdf') as img1:
    print img1.width
    print img1.height
    

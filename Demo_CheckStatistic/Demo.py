# -*- coding: utf8 -*-
'''
Created on Feb 26, 2016
@author: JuniorK
'''
import sys
import cv2
import numpy as np
import DeSkew
map={0:"NUlL",1:'không hoàn thành',2:'hoàn thành',3:'tốt',4:'xuất sắc'}
#map={0:0,1:1,2:2,3:3,4:4}
def Find_Tab(src_im):
    #print 'Find table.....'
    #src_im=cv2.medianBlur(src_im,5)
    src_im=cv2.pyrDown(src_im)
    gray_im=cv2.cvtColor(src_im,cv2.COLOR_RGB2GRAY)
    skewed_im=DeSkew.deskew_base_moment(gray_im)
    #skewed_im=gray_im
    he,wi= skewed_im.shape[:2] 
    #_,bin_im=cv2.threshold(skewed_im,200,255,0)
    
    bin_im=cv2.adaptiveThreshold(skewed_im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
                
    kernel = np.ones((5,5),np.uint8)
    bin_im = cv2.erode(bin_im,kernel,iterations = 1)
    #cv2.imshow("",cv2.pyrDown(bin_im))
    #cv2.waitKey(0)
    
    
    contour,_=cv2.findContours(bin_im,1,2)
    s_max=0
    for c in contour:
        x,y,w,h=cv2.boundingRect(c)
        #cv2.rectangle(skewed_im,(x,y),(x+w,y+h),(222,0,0),2)
        if (w*h<0.95*(he*wi)):
            if w*h>s_max:
                s_max=w*h
                res=(x,y,w,h)
          
    res_im=skewed_im[res[1]:res[1]+res[3],res[0]:res[0]+res[2]]
    #cv2.imwrite('o.png',skewed_im)
    return res_im
def Split_Tab(src_im):
    #print 'Split table.....'
    res_arr=[]
    #src_im=cv2.pyrDown(src_im)  ######
    x=src_im
    kernel = np.ones((3,3),np.uint8)
    #_,src_im=cv2.threshold(src_im,200,255,0)
    src_im=cv2.adaptiveThreshold(src_im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    src_im___ = cv2.erode(src_im,kernel,iterations = 1)
    cv2.imwrite("x.png",src_im___)
    #cv2.waitKey(0)
    h,w=src_im.shape[:2]
    i=0
    cnt_im=0
    cur_pos=0
    pre_pos=0
    while i<h:
        cnt_px=0
        for j in range(w):
            cnt_px+=(src_im___[i][j]==0)           ###
        if cnt_px>=0.5*w:
            #cv2.line(x,(0,i),(w,i),(255,222,0),2)
            cur_pos=i
            delta=(cur_pos-pre_pos)
            sub_im=src_im[pre_pos+int(delta*0.15):cur_pos-int(delta*0.05),0:w]         ############
            pre_pos=cur_pos
            #cv2.imwrite('sub'+str(cnt_im)+'.png',sub_im)
            res_arr.append(sub_im)
            cnt_im+=1
            i+=20       ########
        i+=1
    return res_arr
def Recognise_SubTab(subtab_arr):
    res=''
    #print 'Recognise.....'
    for x in range(2,len(subtab_arr)):
        sub_im=subtab_arr[x]
        #cv2.imshow("",sub_im)
        #cv2.waitKey(0)
        h,w=sub_im.shape[:2]
        j=w-1
        cur_pos=w-1
        pre_pos=w-1
        cnt_im=0
        pos=0
        max_px_area=0
        while j>0:
            cnt_px=0
            for i in range(h):
                cnt_px+=sub_im[i][j]==0
            if cnt_px>=0.9*h:
                cur_pos=j
                delta=(pre_pos-cur_pos)
                sub_field=sub_im[3:h-3,cur_pos+int(0.02*delta):pre_pos-int(0.05*delta)]           #############   
                d=cv2.countNonZero(sub_field)
                h_sub,w_sub=sub_field.shape[:2]
                cnt_px_sub= (h_sub*w_sub)-d
                if cnt_im>0 and cnt_im<5:                 #################
                    if (cnt_px_sub>max_px_area) : 
                        max_px_area=cnt_px_sub
                        pos=cnt_im                     
                #cv2.imwrite(str(x)+'_'+str(cnt_im)+'.png',sub_field)
                #cv2.imshow(str(x)+'_'+str(cnt_im)+'.png',sub_field)
                pre_pos=cur_pos
                cnt_im+=1
                j-=10   #################
            if (cnt_im>5) : break           #########
            j-=1  
        #print '{0}   {1}'.format(x-2,map[pos])
        res+=str(x-1)+'_'+str(map[pos])+'|'
        #print map[pos]   
    return res
if __name__ == "__main__":   
    #img=cv2.imread(sys.argv[1])
    img=cv2.imread('test01.png')
    tab=Find_Tab(img)
    subtab_arr=Split_Tab(tab)
    print Recognise_SubTab(subtab_arr)





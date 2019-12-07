from __future__ import print_function
from PIL import Image
import numpy as np
import cv2 as cv
from imutils.object_detection import non_max_suppression
from imutils import paths
import argparse
import imutils
import sys
import datetime
t_stamp=datetime.datetime.now()
t_stamp=str(t_stamp.minute)+'-'+str(t_stamp.second)
port_name=t_stamp+'portrait.jpg'
cs=t_stamp+'colorsplash.jpg'
print(port_name)
class App():
    BLUE = [255,0,0]        # rectangle color
    RED = [0,0,255]         # PR BG
    GREEN = [0,255,0]       # PR FG
    BLACK = [0,0,0]         # sure BG
    WHITE = [255,255,255]   # sure FG

    DRAW_BG = {'color' : BLACK, 'val' : 0}
    DRAW_FG = {'color' : WHITE, 'val' : 1}
    DRAW_PR_FG = {'color' : GREEN, 'val' : 3}
    DRAW_PR_BG = {'color' : RED, 'val' : 2}

    #setting up flags
    rect = (0,0,1,1)
    
    drawing = False         # flag for drawing curves
    rectangle = False       # flag for drawing rect
    rect_over = False       # flag to check if rect drawn
    rect_or_mask = 100      # flag for selecting rect or mask mode
    value = DRAW_FG         # drawing initialized to FG
    thickness = 3           # brush thickness

    def onmouse(self, event, x, y, flags, param):
        # Draw Rectangle
        if event == cv.EVENT_RBUTTONDOWN:
            self.rectangle = True
            self.ix, self.iy = x,y

        elif event == cv.EVENT_MOUSEMOVE:
            if self.rectangle == True:
                self.img = self.img2.copy()
                cv.rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
                self.rect = (min(self.ix, x), min(self.iy, y), abs(self.ix - x), abs(self.iy - y))
                self.rect_or_mask = 0

        elif event == cv.EVENT_RBUTTONUP:
            self.rectangle = False
            self.rect_over = True
            cv.rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
            self.rect = (min(self.ix, x), min(self.iy, y), abs(self.ix - x), abs(self.iy - y))
            self.rect_or_mask = 0
            
            
        # draw touchup curves

        if event == cv.EVENT_LBUTTONDOWN:
            if self.rect_over == False:
                print("first draw rectangle \n")
            else:
                self.drawing = True
                cv.circle(self.img, (x,y), self.thickness, self.value['color'], -1)
                cv.circle(self.mask, (x,y), self.thickness, self.value['val'], -1)

        elif event == cv.EVENT_MOUSEMOVE:
            if self.drawing == True:
                cv.circle(self.img, (x, y), self.thickness, self.value['color'], -1)
                cv.circle(self.mask, (x, y), self.thickness, self.value['val'], -1)

        elif event == cv.EVENT_LBUTTONUP:
            if self.drawing == True:
                self.drawing = False
                cv.circle(self.img, (x, y), self.thickness, self.value['color'], -1)
                cv.circle(self.mask, (x, y), self.thickness, self.value['val'], -1)

    def run(self):
        # Loading images
        if len(sys.argv) == 2:
            filename = sys.argv[1] # for drawing purposes
        else:
            #Enter your File name
            filename = 'gold.jpg'

        self.img = cv.imread(cv.samples.findFile(filename))
        self.img = cv.resize(self.img,(self.img.shape[1],self.img.shape[0]))
        #use this if image is too large
        #self.img = cv.resize(self.img,(1024,768))
        self.img2 = self.img.copy()                               # a copy of original image
        self.mask = np.zeros(self.img.shape[:2], dtype = np.uint8) # mask initialized to PR_BG
        self.output = np.zeros(self.img.shape, np.uint8)           # output image to be shown

        #output windows
       
        cv.namedWindow('input')
        cv.setMouseCallback('input', self.onmouse)
        cv.moveWindow('input', self.img.shape[1]+10,90)

        print(" Instructions: \n")
        print(" Draw a rectangle around the object using right mouse button \n")
        print("Double tap q when you've finished it will save your image \n Paint with left mouse button for more accuracy")
        
        
        while(1):
            k=cv.waitKey(1)
            if k==ord('q'):
                cv.imwrite(port_name,port)
                cv.imwrite(cs,dst)
                print("done")
                break
            i=0
            i=i+1
            
            
            
            cv.imshow('input', self.img)
            k = cv.waitKey(1)
            k=ord('n')

            # key bindings   
             # segment the image
            
     
            try:
                    if (self.rect_or_mask == 0):         # grabcut with rect
                        bgdmodel = np.zeros((1, 65), np.float64)
                        fgdmodel = np.zeros((1, 65), np.float64)
                        #print(self.rect)
                       
                        cv.grabCut(self.img2, self.mask, self.rect, bgdmodel, fgdmodel, 1, cv.GC_INIT_WITH_RECT)
                        self.rect_or_mask = 1
                    elif self.rect_or_mask == 1:         # grabcut with mask
                        bgdmodel = np.zeros((1, 65), np.float64)
                        fgdmodel = np.zeros((1, 65), np.float64)
                      
                        
                        cv.grabCut(self.img2, self.mask, self.rect, bgdmodel, fgdmodel, 1, cv.GC_INIT_WITH_MASK)
            except:
                    import traceback
                    #traceback.print_exc()
                    #print("Found EXCEPTION")
            
            mask2 = np.where((self.mask==1) + (self.mask==3), 255, 0).astype('uint8')
            #portrait code starts here
            blur=cv.GaussianBlur(self.img2,(21,21),4)
            self.output = cv.bitwise_and(self.img2,self.img2, mask=mask2)
            mask_inv=cv.bitwise_not(mask2)
            img=cv.bitwise_and(blur,blur,mask=mask_inv)
            img2=cv.bitwise_and(self.img2,self.img2, mask=mask2)
            
            port=cv.add(img,img2)
             #for displaying portrait
            cv.imshow("PORTRAIT",port)
            #color splash starts from here
            img=self.img2.copy()
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
            img1 = cv.cvtColor(img, cv.COLOR_GRAY2BGR)    
            img2 = img2.copy()
            img2gray = cv.cvtColor(img2,cv.COLOR_BGR2GRAY)
            ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
            mask_inv = cv.bitwise_not(mask) 
           
            img1_bg = cv.bitwise_and(img1, img1, mask = mask_inv)
           
            img2_fg = cv.bitwise_and(img2, img2, mask = mask)
            k = cv.waitKey(1)
            dst = cv.add(img1_bg,img2_fg)
            #for displaying colorsplash
            cv.imshow('COLOR_SPLASH',dst)
            
          
            
     

if __name__ == '__main__':
    print(__doc__)
    App().run()
    cv.destroyAllWindows()

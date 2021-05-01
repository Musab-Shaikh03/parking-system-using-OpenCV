import cv2
import numpy as np

min_contour_width=80  #40
min_contour_height=80  #40
offset=10       #10
line_height=550 #550
matches =[]
cars=0
cars1=0
Total=0
total_space = 50
final_total = 15
def get_centroid(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1
    return cx,cy
    #return (cx, cy)
        
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('sample.mp4')
#cap = cv2.VideoCapture('Relaxing highway traffic.mp4')



cap.set(3,1920)
cap.set(4,1080)

if cap.isOpened():
    ret,frame1 = cap.read()
else:
    ret = False
ret,frame1 = cap.read()
ret,frame2 = cap.read()
    
while ret:
    ret, frame2 = cap.read()
    frame= frame2.copy()
    gray=cv2.absdiff(frame1,frame2)
    blur = cv2.GaussianBlur(gray,(9,9),0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    _,thresh =cv2.threshold(gray,50,255,cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh,np.ones((7,7)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (12, 12))
        # Fill any small holes
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    contours,h = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for(i,c) in enumerate(contours):
        (x,y,w,h) = cv2.boundingRect(c)
        contour_valid = (w >= min_contour_width) and (h >= min_contour_height)

        if not contour_valid:
            continue
        cv2.rectangle(frame,(x-10,y-10),(x+w+10,y+h+10),(255,0,0),2)
        
        cv2.line(frame, (600, line_height), (1200, line_height), (0,255,0), 2)
        cv2.line(frame, (0, line_height), (550, line_height), (0,255,0), 2)
        centroid = get_centroid(x, y, w, h)
        matches.append(centroid)
        cv2.circle(frame,centroid, 5, (0,255,0), -1)
        cx,cy= get_centroid(x, y, w, h)
        for (x,y) in matches:
            if y<(line_height+offset) and y>(line_height-offset):
                if 600<x<1200:
                    cars+=1
                    final_total -= 1
                    matches.remove((x,y))
                    print('enter',cars)
                if 0<x<600:
                    cars1+=1
                    final_total += 1
                    matches.remove((x,y))
                    print('exit',cars1)
            Total=cars+cars1
            
            #output in text file
            count=open('test.txt','w')
            print(str(final_total),file = count,end="")
            count.close()
            
    cv2.putText(frame, "Cars entered: " + str(cars), (940, 90), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 170, 0), 2)
    cv2.putText(frame, "Spaces Available: " + str(final_total), (940, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 170, 0), 2)
    cv2.putText(frame, "Cars exit: " + str(cars1), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 170, 0), 2)
    cv2.putText(frame, "Total: " + str(Total), (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 170, 0), 2)
    cv2.drawContours(frame,contours,-1,(0,0,255),2)


    cv2.imshow("Original" , frame)
    if cv2.waitKey(1) == 27:
        break
    frame1 = frame2
#print(matches)    
cv2.destroyAllWindows()
cap.release()

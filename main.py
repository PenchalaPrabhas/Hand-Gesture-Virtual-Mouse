import cv2
import mediapipe as mp
import detect
import numpy as np
import autopy
import time

ctime=time.time()
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands=mp_hands.Hands()
cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 7
timer=0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
wScr, hScr = autopy.screen.size()
ulist=[]
mlist=[]
r=0 
g=100 
b=255
ctime=int(ctime)
def movement(mylmList):
                                x1, y1 = mylmList[8][1:]
                                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                                clocX = plocX + (x3 - plocX) / smoothening
                                clocY = plocY + (y3 - plocY) / smoothening
                                
                                autopy.mouse.move(wScr - clocX, clocY)
                                return clocX, clocY
        
while True:
    timer = cv2.getTickCount()
    success, image = cap.read()
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h,w,c=image.shape
    r+=1
    g+=1
    b+=1
    frame_height, frame_width, _ = image.shape                                                     
    
    results = hands.process(imgRGB)
   
    
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    if r>=255:
            r=0
    if g>=255:
            g=0
    if b>=255:
            b=0

    cv2.rectangle(image, (frameR, frameR), (wCam - 100, hCam - 100),(r,g,b), 2)
    
    label="No hands"
    if results.multi_hand_landmarks:
       
        for handType, handLms in zip(results.multi_handedness, results.multi_hand_landmarks):
                mylmList = []

                
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([id,px, py])
                
                #print(handType.classification[0].label,"+" ,mylmList)#getting 21 points
                
                uplist=detect.fingersUp(mylmList)
                
                if len(results.multi_handedness) == 2: 
                        
                        if handType.classification[0].label == "Left":
                                ulist=uplist
                                mlist=mylmList
                                
                        elif len(mlist)!=0:
                                if uplist==[0,1,1,1,1] and ulist==[1,1,1,1,1] :
                                        plocX, plocY = movement(mlist)
                                if uplist==[0,1,1,1,1] and ulist==[0,1,1,1,1]:
                                        detect.click()
                                        pass
                              
                                if (ulist==[0,1,0,0,0] or ulist==[1,1,0,0,0]) and  uplist==[0,1,0,0,0]:
                                        
                                        length, image, lineInfo =detect.findDistance(8, 8, image,mylmList,mlist)
                               
                                        if length> 390:
                                                
                                                cv2.line(image,mylmList[8][1:], mlist[8][1:], (0, 255, 0), 2)
                        
                                                ctime=detect.both(True,ctime)
                    
                                        elif length<170:
                                                cv2.line(image,mylmList[8][1:], mlist[8][1:], (255, 0, 0), 2)
                                                ctime=detect.both(False,ctime)
                                elif((ulist==[0,1,1,0,0] or ulist==[1,1,1,0,0]) and  uplist==[0,1,1,0,0]):
                                                xa,ya=mylmList[12][1:]
                                                xb,yb= mlist[12][1:]
                                                length, image, lineInfo =detect.findDistance(12, 12, image,mylmList,mlist)
                                                if abs(ya-yb)>30:
                                                        cv2.line(image,mylmList[12][1:], mlist[12][1:], (0, 255, 255), 2)
                                  
                                                        detect.scrol(ya-yb)
                                
                                else:
                                        detect.bothhands(uplist,ulist)
                                        
                             
                                        
                        label="both hands"
                elif handType.classification[0].label == "Right":# detecting two hands. left or right
                       label = "Left hand"
                else:
                        label = "Right hand"
                        
                        if uplist==[0,1,0,0,0] or uplist==[0,1,1,0,0] :
                                
                                
                                plocX, plocY = movement(mylmList)
                        if uplist==[0,1,1,0,0] or uplist==[0,1,1,0,0]:
        
                                length, img, lineInfo = detect.findDistance(8, 12, image,mylmList,mylmList)
                                
        
                                if length < 40:
                                        cv2.circle(img, (lineInfo[4], lineInfo[5]),15, (0, 255, 0), cv2.FILLED)
                                        detect.dc()
                        
                                
                                
                        else:
                           
                                ctime=detect.right(uplist,ctime)
                                
               
                mp_drawing.draw_landmarks(image, handLms,mp_hands.HAND_CONNECTIONS)

        
    image = cv2.flip(image, 1) 
    cv2.putText(image, label, (frameR-5,frameR-5), cv2.FONT_HERSHEY_COMPLEX, 0.9, (3,255,5), 2)
    cv2.putText(image,"FPS: "+str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2);
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(1) & 0xFF == ord('a'):
        break
cv2.destroyAllWindows()

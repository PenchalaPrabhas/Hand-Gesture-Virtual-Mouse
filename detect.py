#
import pyautogui
import cv2
import math
import time
def findDistance(p1, p2, img,lmList,lmlist1):
     
        x1, y1 = lmList[p1][1:]
        x2, y2 = lmlist1[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return int(length), img, [x1, y1, x2, y2, cx, cy]
def fingersUp(lmList):
        fingers = []
        tipIds = [4, 8, 12, 16, 20]
        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):

            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # totalFingers = fingers.count(1)

        return fingers
def bothhands(ulist,uplist):
    print(ulist,uplist)
    if (ulist==[0,0,1,1,1] or ulist==[1,0,1,1,1]) and (uplist==[0,0,0,1,1] or uplist==[1,0,0,1,1]):
        pyautogui.keyDown('ctrl')  
        pyautogui.press('c')     #cpy
        pyautogui.keyUp('ctrl')  
        time.sleep(1)
        print("copy")
    elif (ulist==[0,0,1,1,1] or ulist==[1,0,1,1,1]) and  (uplist==[0,0,0,0,1] or uplist==[1,0,0,0,1]):
        pyautogui.keyDown('ctrl')  
        pyautogui.press('x')    #cut
        pyautogui.keyUp('ctrl')  
        time.sleep(1)
        print("cut")
    elif (ulist==[0,0,1,1,1] or ulist==[1,0,1,1,1] )and  (uplist==[0,0,1,1,1] or uplist==[1,0,1,1,1]):
        pyautogui.keyDown('ctrl')  
        pyautogui.press('v')  #paste
        pyautogui.keyUp('ctrl')  
        time.sleep(1)
        print("paste")
    elif ulist==[1,1,0,0,1] or ulist==[0,1,0,0,1] and  uplist==[0,1,0,0,1] or uplist==[1,1,0,0,1]:
        current_time = time.time()
        formatted_time = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(current_time))
        sc=formatted_time+"sc.png"
        screenshot = pyautogui.screenshot()
      
        screenshot.save(sc)
        print(sc)
        time.sleep(2)
    elif ulist==[0, 1, 1, 1, 1] and uplist==[0, 0, 0, 0, 0]:
        pyautogui.keyDown('ctrl')  
        pyautogui.press('z')  #paste
        pyautogui.keyUp('ctrl')  
        time.sleep(1)
        print("undo")
        
    
def right(uplist,ctime):
    ptime=time.time()
    ptime=int(ptime)
    
    if ctime>ptime:
        return ctime
    if uplist==[0,1,1,0,1] or uplist==[1,1,1,0,1]:
        dc()
    if uplist==[1,1,1,0,0]:
        click()
   
    if uplist==[0,0,1,0,0] or uplist==[1,0,1,0,0]:
        pyautogui.click(button='right', clicks=1, interval=0.5)
    if uplist==[0,1,0,0,0] or uplist==[1,1,0,0,0]:
        pyautogui.click(button='left', clicks=1, interval=0.5)
        
    
        
        
    return ptime
def dc():
    pyautogui.doubleClick(interval=0.5)
    #   right,left
def both(length,ctime):
    ptime=time.time()
    ptime=int(ptime)
    
    if ctime>ptime:
        return ctime
    if length:
        pyautogui.keyDown('ctrl')  
        pyautogui.press('+')  
        pyautogui.keyUp('ctrl')   
        
    else:
        pyautogui.keyDown('ctrl')  
        pyautogui.press('-')  
        pyautogui.keyUp('ctrl')   
        
    return ptime+1
        
def scrol(length):
    
    pyautogui.scroll(length)
def click():
    pyautogui.click(clicks=1, interval=0.5)
def move(x):
    if x:
        pyautogui.mouseDown()
    else:
        pyautogui.mouseUp()
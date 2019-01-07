import cv2
import pyautogui

cap = cv2.VideoCapture(0)
ct = 0
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
colour = [(0, 255, 0), (0, 0, 255) ]
toggle = 1
facelocation = (100,100,100,100)
cent = [0,0]
x_bef = 0

   
def reset():
    global ct
    global toggle
    global x_bef
    x_bef = 0
    toggle = 1
    ct = 0
    
def centered(x,y,w,h):
    x_cent = x+(w/2)
    y_cent = y+(h/2)
    return [int(x_cent), int(y_cent)]

while(True):
    
    ret, frame = cap.read()

    faces = faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )
    
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, (36, 75, 65), (70, 255,255))
    blur =  cv2.medianBlur(mask, 15)
    _, contour, _ = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for (x, y, w, h) in faces:
        if toggle == 0:
            continue
        facelocation = (x,y,w,h)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        
    if len(contour) != 0:
        c = max(contour, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        if w > 25 :
            cent = centered(x,y,w,h)
            cv2.circle(frame, (cent[0], cent[1]), 4, colour[toggle], -1)
    else :
        reset()
        cent = [0,0]
    
    if cent[1] >= facelocation[1] and cent[1] <= facelocation[1]+facelocation[3]:
        toggle = 0
        if x_bef:
            dX = cent[0]-x_bef
        else:       
            dX = 0
        if dX < -30:
            ct+=1
        elif dX > 30:
            ct-=1
        else:
            ct = 0
        x_bef = cent[0]
    else :
        reset()
    
    if ct > 3:
        pyautogui.press('left')
        print('A')
        reset()
    elif ct <-3:
        pyautogui.press('right')
        print('B')
        reset()

    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
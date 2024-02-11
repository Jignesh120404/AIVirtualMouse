import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawings = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
video = cv2.VideoCapture(0)
x1 = x2 = y1 = y2=0
while video.isOpened():
    ret, frame = video.read()
    frame = cv2.flip(frame,1)
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for idx, landmark in enumerate(hand_landmarks.landmark):
                height, width, _ = frame.shape
                cx, cy = int(landmark.x * width), int(landmark.y * height)
                #print(f"X:{cx} Y:{cy}")
                mp_drawings.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                if idx ==8:
                    mouse_x = int(screen_width/width*cx)
                    mouse_y = int(screen_height/height*cy)
                    pyautogui.moveTo(mouse_x,mouse_y)
                    cv2.circle(frame,(cx,cy),10,(0,255,255))
                    x1 =cx
                    y1 =cy
                if idx ==4:
                    x2 =cx
                    y2 =cy
                    cv2.circle(frame,(cx,cy),10,(0,255,255))
                    
        dist = y2-y1
        #print(dist)
        if (dist<20) :
            pyautogui.click()  
                    
    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

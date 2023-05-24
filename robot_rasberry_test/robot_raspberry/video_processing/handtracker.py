import mediapipe
 
import cv2




def detect_hand(frame):
    drawingModule = mediapipe.solutions.drawing_utils
    handsModule = mediapipe.solutions.hands
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:
        #flipped = cv2.flip(frame, flipCode = 1)
        #frame1 = cv2.resize(flipped, (320, 240))
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)
                
        return frame
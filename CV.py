import cv2
import mediapipe as mp
import serial
import time

# Initialize Arduino serial communication
arduino = serial.Serial('COM8', 9600)
time.sleep(2)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Fingertip landmark IDs for fingers
finger_tips = [4, 8, 12, 16, 20]

# Open webcam
cap = cv2.VideoCapture(1)
prev_count = -1

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    finger_count = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]

            # Thumb (checks if it's open)
            if lm_list[finger_tips[0]][0] > lm_list[finger_tips[0] - 1][0]:
                finger_count += 1

            # Other fingers (index to pinky)
            for id in finger_tips[1:]:
                if lm_list[id][1] < lm_list[id - 2][1]:
                    finger_count += 1

            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Send data to Arduino only if finger count changes
    if finger_count != prev_count:
        arduino.write(str(finger_count).encode())
        prev_count = finger_count

    # Display finger count on screen
    cv2.putText(frame, f"Fingers: {finger_count}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
    cv2.imshow("Hand Gesture LED Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
arduino.close()

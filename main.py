import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands
hands_module = mp.solutions.hands
hands_detector = hands_module.Hands()
drawing_utils = mp.solutions.drawing_utils

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Initialize video capture
cap = cv2.VideoCapture(0)

index_y = 0

while True:
    frame_captured, image_frame = cap.read()
    if not frame_captured:
        print("Ignoring empty camera frame.")
        continue

    # Flip the frame horizontally for a later selfie-view display
    image_frame = cv2.flip(image_frame, 1)
    frame_height, frame_width, _ = image_frame.shape
    rgb_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB)
    output = hands_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            # Draw hand landmarks
            drawing_utils.draw_landmarks(image_frame, hand, hands_module.HAND_CONNECTIONS)
            for id, landmark in enumerate(hand.landmark):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                
                # Index finger tip (id == 8)
                if id == 8:
                    cv2.circle(img=image_frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=-1)
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                
                # Thumb tip (id == 4)
                if id == 4:
                    cv2.circle(img=image_frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=-1)
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    print('Distance between index and thumb:', abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 20:
                        try:
                            pyautogui.click()
                            pyautogui.sleep(1)
                        except Exception as e:
                            print(f"Error during click: {e}")
                    elif abs(index_y - thumb_y) < 100:
                        try:
                            pyautogui.moveTo(index_x, index_y)
                        except Exception as e:
                            print(f"Error during move: {e}")

    cv2.imshow('Virtual Mouse', image_frame)
    
    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()


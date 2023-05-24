import cv2
import dlib
import time
import matplotlib.pyplot as plt
from gaze_tracking import GazeTracking

# dlib의 얼굴 인식기 생성
detector = dlib.get_frontal_face_detector()
# 얼굴 방향 예측기 생성
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
# 눈의 움직임 추적기 생성
gaze = GazeTracking()

# 웹캠 열기
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# Initialize the time and text lists
times = []
texts = []
center_gaze_intervals = []

# Initialize variables to track gaze duration
center_gaze_start_time = None
center_gaze_duration = 0

print('카메라를 바라보세요. 3초 후 얼굴을 인식합니다.')
for i in range(3, 0, -1):
    print(i)
    cv2.waitKey(1000)

while True:
    ret, frame = cap.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # 얼굴 인식
    faces = detector(small_frame)
    # 눈의 움직임 추적
    gaze.refresh(frame)

    if len(faces) > 0:
        landmarks = predictor(small_frame, faces[0])
        left_eye = landmarks.part(36)
        right_eye = landmarks.part(45)
        nose = landmarks.part(30)

        # 눈과 코의 위치를 이용하여 얼굴 방향 예측
        if left_eye.x < nose.x and right_eye.x > nose.x:
            print('정면을 바라보고 있습니다.')
            for i in range(68):
                x = landmarks.part(i).x * 2
                y = landmarks.part(i).y * 2
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
        else:
            print('정면을 바라보세요.')

        # 눈의 움직임에 따른 메시지 출력
        text = ""
        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            text = "Looking right"
        elif gaze.is_left():
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"
        print(text)
    else:
        print('얼굴이 인식되지 않았습니다.')

    # 이미지 출력
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

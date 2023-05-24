import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # 이미지 전처리
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    gray = cv2.medianBlur(gray, 7)

    # 얼굴 인식 처리
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # 동공 인식 처리
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            # 동공 중심점 좌표 계산
            cx = ex + ew // 2
            cy = ey + eh // 2
            # 동공 중심점 표시
            cv2.circle(roi_color, (cx, cy), 2, (0, 0, 255), -1)

            # 눈동자 인식 처리
            iris_w = int(ew * 0.5)
            iris_h = int(eh * 0.5)
            iris_x = ex + int(ew * 0.25)
            iris_y = ey + int(eh * 0.25)

            iris_roi_gray = roi_gray[iris_y:iris_y + iris_h, iris_x:iris_x + iris_w]
            _, iris_thresh = cv2.threshold(iris_roi_gray, 40, 255, cv2.THRESH_BINARY)

            contours, _ = cv2.findContours(iris_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

            for cnt in contours:
                (x, y, w, h) = cv2.boundingRect(cnt)
                cx_iris = iris_x + x + w // 2
                cy_iris = iris_y + y + h // 2
                # 눈동자 중심점 표시
                cv2.circle(roi_color, (cx_iris, cy_iris), 2, (0, 255, 0), -1)
                break

            # 눈동자 중심점과 동공 중심점 간의 거리 계산
            dx = cx_iris - cx
            dy = cy_iris - cy
            dist = np.sqrt(dx ** 2 + dy ** 2)

            # 일정 거리 이상 벗어난 경우 "집중하세요!" 문구 표시
            if dist > 30:
                cv2.putText(frame, "집중하세요!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                break

    # 동공, 눈동자 인식 결과 출력
    cv2.imshow('Pupil Detection', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

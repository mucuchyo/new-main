import cv2
from gaze_tracking import GazeTracking
import matplotlib.pyplot as plt
import time

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

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

while True:
    # Get a new frame from the webcam
    _, frame = webcam.read()

    # Analyze the frame using GazeTracking
    gaze.refresh(frame)

    # Get the annotated frame with text
    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

        # If starting a new center gaze interval
        if center_gaze_start_time is None:
            center_gaze_start_time = time.time()

        center_gaze_duration = time.time() - center_gaze_start_time

    else:
        # If ending a center gaze interval
        if center_gaze_start_time is not None:
            center_gaze_intervals.append(center_gaze_duration)

        center_gaze_start_time = None
        center_gaze_duration = 0

    # Add the current time and text to the lists
    times.append(time.time())
    texts.append(text)

    # Draw the text and pupil coordinates on the frame
    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    # Write the frame to the output video
    out.write(frame)

    # Show the frame
    cv2.imshow("Demo", frame)

    # Exit on 'q' keypress
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and writer objects
webcam.release()
out.release()
cv2.destroyAllWindows()

# Plot the text as a function of time
plt.plot(times, texts)
plt.xlabel('Time (seconds)')
plt.ylabel('Text')
plt.show()

# Display the duration of center gaze intervals

total_duration = times[-1] - times[0]
not_center_duration = total_duration - sum(center_gaze_intervals)
print("영상 전체의 시간 {:.2f} 초 중 {:.2f} 초간 집중하지 못하셨습니다.".format(total_duration, not_center_duration))
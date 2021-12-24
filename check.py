import cv2
video_capture = cv2.VideoCapture(0)
video_capture.set(3, 1280)
video_capture.set(4, 720)

while True:
    suceess, frame = video_capture.read()
    cv2.imshow("image", frame)
    cv2.waitKey(0)
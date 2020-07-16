import cv2
import sys
import os



face_cascade_path = '/usr/local/opt/opencv/share/'\
                    'opencv4/haarcascades/haarcascade_frontalface_default.xml'
eye_cascade_path = '/usr/local/opt/opencv/share/'\
                   'opencv4/haarcascades/haarcascade_eye.xml'

cascade_path = 'cascade/cascade.xml'



face_cascade = cv2.CascadeClassifier(face_cascade_path)
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
cascade = cv2.CascadeClassifier(cascade_path)

capture = cv2.VideoCapture(0)

while True:
    ret,src = capture.read()
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(src_gray)
    for x, y, w, h in faces:
        cv2.rectangle(src, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = src[y: y + h, x: x + w]
    #    face_gray = src_gray[y: y + h, x: x + w]
    #    eyes = eye_cascade.detectMultiScale(face_gray)
    #    for (ex, ey, ew, eh) in eyes:
    #       cv2.rectangle(face, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    cv2.imshow("Detection",src)

    c = cv2.waitKey(1)

    if c == 27:
        break


capture.release()
cv2.destroyAllWindows()
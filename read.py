import cv2
import sys
import os
import numpy as np
from pdf2image import convert_from_path

cascade_path = 'keisanki/keenest/cascade.xml'

cascade = cv2.CascadeClassifier(cascade_path)

change = convert_from_path('pdf_samples/scan_kuma.pdf')
change[0].save('middle.png','png')

image = cv2.imread('middle.png')

img_gray_sub = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
img_gray = cv2.adaptiveThreshold(img_gray_sub,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
detected = cascade.detectMultiScale(img_gray)

print(len(detected))
print(detected)

detected_list = []

for i in detected:
    if i[2] >= 55 or i[3] >= 55 or i[2] <= 25 or i[2] <= 25:
        continue
    else:
        detected_list.append(i)

print(len(detected_list))

for li in detected_list:
        cv2.rectangle(image, (li[0], li[1]), (li[0] + li[2], li[1] + li[3]), (255, 0, 0), 2)

cv2.namedWindow("detected",cv2.WINDOW_AUTOSIZE)
cv2.imshow('detected',image)

c = cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('result.png',image)

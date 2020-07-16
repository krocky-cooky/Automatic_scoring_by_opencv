import cv2
import os 
import sys
import math
import pyocr
from PIL import Image
import time
from pdf2image import convert_from_path

tools = pyocr.get_available_tools()
tool = tools[0]

cascade_path = 'keenest/cascade.xml'

cascade = cv2.CascadeClassifier(cascade_path)

change = convert_from_path('scan.pdf')
change[0].save('middle.png','png')


image = cv2.imread('middle.png')

img_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
detected = cascade.detectMultiScale(img_gray)

def dist(a,b):
    distant = math.pow(a[0]-b[0],2)+math.pow(a[1]-b[1],2)
    return distant

set_list = []
detected_list = []
for i in detected:
    if i[2] >= 55 or i[3] >= 55 or i[2] <= 25 or i[3] <= 25:
        continue
    else:
        detected_list.append(i)


done= []

for li in detected_list:
    distant = {}
    k = False
    for x in done:
        if all(li == x):
            k = True
    if k:
        continue
    for i,sub in enumerate(detected_list):
        distant[i] = dist(li,sub)
    
    sorted_distant = sorted(distant.items(),key=lambda x:x[1])
    get = []
    for j in range(6):
        get.append(detected_list[sorted_distant[j][0]])
        done.append(detected_list[sorted_distant[j][0]])
    set_list.append(get)
ans_list = []

print(len(set_list))

for i,li in enumerate(set_list):
    up_or_down_sort = sorted(li,key = lambda x:x[1]) 
    upper = up_or_down_sort[0:3]
    bottom = up_or_down_sort[3:6]
    sorted_upper = sorted(upper,key=lambda x:x[0])
    sorted_bottom = sorted(bottom,key=lambda x:x[0])
    #cutted_image = img_grey[upper[0][1]+upper[0][3]:bottom[0][1],]
    image_num = image[sorted_upper[0][1]+sorted_upper[0][3]:sorted_bottom[1][1],sorted_upper[0][0]+sorted_upper[0][2]:sorted_bottom[1][0]]
    image_ans = image[sorted_upper[1][1]+sorted_upper[1][3]:sorted_bottom[2][1],sorted_upper[1][0]+sorted_upper[1][2]:sorted_bottom[2][0]]
    cv2.imwrite('image_num' + str(i) + '.png',image_num)
    cv2.imwrite('image_ans' + str(i) + '.png',image_ans)
    
    q_num = tool.image_to_string(
        Image.open('image_num' + str(i) + '.png'),
        lang='eng',
        builder = pyocr.builders.DigitBuilder(tesseract_layout=7)
    )
    ans_num = tool.image_to_string(
        Image.open('image_ans' + str(i) + '.png'),
        lang='eng',
        builder = pyocr.builders.DigitBuilder(tesseract_layout=7)
    )

    ans_list.append((q_num,ans_num))
    cv2.rectangle(image,(sorted_upper[0][0]+sorted_upper[0][2],sorted_upper[0][1]+sorted_upper[0][3]),(sorted_bottom[1][0],sorted_bottom[1][1]),(250,0,0),2)
    cv2.rectangle(image,(sorted_upper[1][0]+sorted_upper[1][2],sorted_upper[1][1]+sorted_upper[1][3]),(sorted_bottom[2][0],sorted_bottom[2][1]),(250,0,0),2)


sorted_ans_list = sorted(ans_list,key=lambda x:x[0])
print(sorted_ans_list)
cv2.namedWindow("detected",cv2.WINDOW_AUTOSIZE)
cv2.imshow('detected',image)

c = cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('detected_result.png',image)
'''
pdfから採点済みの画像を生成し、点数、正誤、学籍番号を返り値として返す関数が含まれたファイル
ここからsaiten関数をimportして用いた
'''
import cv2
import os 
import sys
import math
import pyocr
from PIL import Image
import time
from pdf2image import convert_from_path
from keisanki import settings #djangoでのsettingsファイル
import numpy as np


ans = [54,112,152,3758] #今回の問題の答え

kernel = np.ones((5,5),np.uint8)

tools = pyocr.get_available_tools() #数字読み取り用のpyocr
tool = tools[0]

cascade_path = settings.BASE_DIR + '/keenest/cascade.xml' #カスケードファイル のパス

cascade = cv2.CascadeClassifier(cascade_path)

def dist(a,b):  #検出された二つのマークの距離を計算する函数
    distance = math.pow(a[0]-b[0],2)+math.pow(a[1]-b[1],2)
    return distance

def saiten(input_url,output_url): #引数はアップロードされたpdfのパスと採点済みの画像を出力するパス。この関数をインポートしてdjangoバックエンド上で処理を行う
    score = 0 #正解した数
    table_dict = {} #それぞれの問題の回答の正誤を辞書型で格納する
    change = convert_from_path(input_url) #pdfをpngに変換
    change[0].save('middle.png','png')
    image = cv2.imread(settings.BASE_DIR + '/middle.png')

    img_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #二値化
    detected = cascade.detectMultiScale(img_gray) #マークの検出



    set_list = [] #近傍6点によって構成されるリストを格納するリスト
    detected_list = [] #検出された値のうち、大きすぎるものや小さすぎるものを取り除いてこのリストに入れる
    for i in detected:
        if i[2] >= 55 or i[3] >= 55 or i[2] <= 25 or i[3] <= 25:
            continue
        else:
            detected_list.append(i)


    done = [] #近傍6点として一度得られたものは再び使われないようにこのリストに入れる
    detected_list.sort(key=lambda x : x[1]) #y座標でソートし上から順にマークを調べていく

    for li in detected_list:
        distant = {}
        k = False
        for x in done:
            if all(li == x):
                k = True
        if k:
            continue
        for i,sub in enumerate(detected_list):
            k = False
            for x in done:
                if all(x == sub):
                    k = True
            if k:
                continue
            distant[i] = dist(li,sub)
    
        sorted_distant = sorted(distant.items(),key=lambda x:x[1])
        get = []
        for j in range(6):
            get.append(detected_list[sorted_distant[j][0]])
            done.append(detected_list[sorted_distant[j][0]])
        set_list.append(get)

    ans_list = [] #読み取った回答を格納する

    for i,li in enumerate(set_list): #６点によって構成されたそれぞれについてy座標によるソートごx座標でソートし6点それぞれの位置を確定し、これによって問題番号と回答を含む部分を切り出す
        up_or_down_sort = sorted(li,key = lambda x:x[1]) 
        upper = up_or_down_sort[0:3]
        bottom = up_or_down_sort[3:6]
        sorted_upper = sorted(upper,key=lambda x:x[0])
        sorted_bottom = sorted(bottom,key=lambda x:x[0])
        #cutted_image = img_grey[upper[0][1]+upper[0][3]:bottom[0][1],]
        image_num = img_gray[sorted_upper[0][1]+sorted_upper[0][3]:sorted_bottom[1][1],sorted_upper[0][0]+sorted_upper[0][2]:sorted_bottom[1][0]]
        image_ans = img_gray[sorted_upper[1][1]+sorted_upper[1][3]:sorted_bottom[2][1],sorted_upper[1][0]+sorted_upper[1][2]:sorted_bottom[2][0]]
        #thres_img_num = cv2.adaptiveThreshold(image_num,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,9,2)
        #thres_img_ans = cv2.adaptiveThreshold(image_ans,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,9,2)
        #cleaned_img_num = cv2.morphologyEx(thres_img_num, cv2.MORPH_OPEN, kernel)
        #cleaned_img_ans = cv2.morphologyEx(thres_img_ans, cv2.MORPH_OPEN, kernel)
        cv2.imwrite('image_num' + str(i) + '.png',image_num)
        cv2.imwrite('image_ans' + str(i) + '.png',image_ans)
    
        q_num = tool.image_to_string( #数字を読み取る
            Image.open(settings.BASE_DIR +'/image_num' + str(i) + '.png'),
            lang='eng',
            builder = pyocr.builders.DigitBuilder(tesseract_layout=7)
        )
        ans_num = tool.image_to_string( #数字を読み取る
            Image.open(settings.BASE_DIR + '/image_ans' + str(i) + '.png'),
            lang='eng',
            builder = pyocr.builders.DigitBuilder(tesseract_layout=7)
        )
    
        if q_num == '0' or not ans_num:
            table_dict[int(q_num)] = 'failed'
        elif ans[int(q_num)-1] == int(ans_num):
            cv2.circle(image,(int((sorted_upper[1][0]+sorted_upper[1][2]+sorted_bottom[2][0])/2),int((sorted_upper[1][1]+sorted_upper[1][3]+sorted_bottom[2][1])/2)),50,(0,0,250),3) #丸付け
            score += 1
            table_dict[int(q_num)] = 'ok'
        else:
            cv2.line(image,(sorted_upper[1][0]+sorted_upper[1][2],sorted_upper[1][1]),(sorted_bottom[2][0],sorted_bottom[2][1]+sorted_bottom[2][3]),(0,0,250),3) #バツ付け
            cv2.line(image,(sorted_bottom[1][0]+sorted_bottom[1][2],sorted_bottom[1][1]+sorted_bottom[1][3]),(sorted_upper[2][0],sorted_upper[2][1]),(0,0,250),3)
            table_dict[int(q_num)] = 'notok'


        ans_list.append((q_num,ans_num))
        #cv2.rectangle(image,(sorted_upper[0][0]+sorted_upper[0][2],sorted_upper[0][1]+sorted_upper[0][3]),(sorted_bottom[1][0],sorted_bottom[1][1]),(250,0,0),2)
        #cv2.rectangle(image,(sorted_upper[1][0]+sorted_upper[1][2],sorted_upper[1][1]+sorted_upper[1][3]),(sorted_bottom[2][0],sorted_bottom[2][1]),(250,0,0),2)


    sorted_ans_list = sorted(ans_list,key=lambda x:x[0])
    print(sorted_ans_list)


#cv2.namedWindow("detected",cv2.WINDOW_AUTOSIZE)
#cv2.imshow('detected',image)

#c = cv2.waitKey(0)
#cv2.destroyAllWindows()
    cv2.imwrite(output_url,image) #outputのパスに画像を保存する
    try:
        student_number = int(sorted_ans_list[0][1])
    except:
        student_number = 0
    return [student_number,score,table_dict] #学籍番号、正解した問題数(点数)、それぞれの問題の正誤を返す
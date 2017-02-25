#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, os
import json, datetime
import logging
import paho.mqtt.client as mqtt
from libraryCH.device.camera import PICamera
from libraryCH.device.lcd import ILI9341

#LCD顯示設定------------------------------------
lcd = ILI9341(LCD_size_w=240, LCD_size_h=320, LCD_Rotate=90)

#拍照設定--------------------------------------
#儲放相片的主目錄
picturesPath = "/var/www/html/farmbot/"
#相機旋轉角度
cameraRotate = 0
#拍攝的相片尺寸
photoSize = (1280, 720)
#一次要連拍幾張
numPics = 3
#間隔幾毫秒
picDelay = 0.5 

#---------------------------------------------------------
#You don't have to modify the code below------------------
#---------------------------------------------------------
camera = PICamera()
camera.CameraConfig(rotation=cameraRotate)  
camera.cameraResolution(resolution=photoSize)

#LCD設定
lcd_LineNow = 0
lcd_lineHeight = 30  #行的高度
lcd_totalLine = 8  # LCD的行數 (320/30=8)
screenSaverNow = False

#logging記錄
logger = logging.getLogger('msg')
hdlr = logging.FileHandler('/home/pi/NDVI/msg.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

#判斷是否為JSON格式
def is_json(myjson):
    try:
        json_object = json.loads(myjson)

    except ValueError:
        return False

    return True

#將行數轉為pixels
def lcd_Line2Pixel(lineNum):
    return lcd_lineHeight*lineNum

#LCD移到下一行, 若超過設定則清螢幕並回到第0行
def lcd_nextLine():
    global lcd_LineNow
    lcd_LineNow+=1
    if(lcd_LineNow>(lcd_totalLine-1)):
        lcd.displayClear()
        lcd_LineNow = 0

def takePictures(saveFolder="others"):
    global picDelay, numPics, picturesPath

    if(os.path.isdir(picturesPath+saveFolder)==False):
        os.makedirs(picturesPath+saveFolder)

    savePath = picturesPath + saveFolder + "/" + str(time.time())
    for i in range(0,numPics):
        camera.takePicture(savePath + "-" + str(i) + ".jpg")
        logger.info("TakePicture " + str(i) + " to " + savePath + "-" + str(i) + ".jpg")
        time.sleep(picDelay)

while True:
#        logger.info("Display logo.")
#        lcd.displayImg("rfidbg.jpg")
    picNum = input("How many pictures you awnt to take? ")

    if(picNum>0):    
        savePath = picturesPath + "pic"
        for i in range(0, picNum):
            camera.takePicture(savePath + "-" + str(i) + ".jpg")
            print('Take picture #{} and save to {}'.format(i,savePath + "-" + str(i) + ".jpg"))
            lcd.displayImg(savePath + "-" + str(i) + ".jpg")
            time.sleep(picDelay)

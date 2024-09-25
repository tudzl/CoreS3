#IIC scan debug code by l.zhou
#proted to CoreS3, need test
#V2.5 improved
#V2.2 ported to core2 
#V2.1 improve display ,  
#V2.0 added loop time display , LCD brightness display
import os, sys, io
from M5 import *
from m5stack_ui import *
from uiflow import *
import  machine
import i2c_bus
import time
import os
import gc

#Btn A: DISPLAY BK light control
def buttonA_wasPressed():
  # global params
  global LCD_EN,image_BG
  image_BG.set_hidden(False)
  #speaker.tone(446, 120, 1)
  #image_BMW = M5Img("res/BMW_coupit BG2.png", x=0, y=0, parent=None)
  LCD_EN = LCD_EN+5
  if LCD_EN > 100:
     LCD_EN = 100
  #else:
  #   LCD_EN = 20 
  wait(0.1)
  pass

#Btn B: DISPLAY BK light control
def buttonB_wasPressed():
  # global params
  global LCD_EN,image_BG
  image_BG.set_hidden(True)
  #speaker.tone(1046, 120, 1)
  LCD_EN = LCD_EN-5
  if LCD_EN <= 0:
     LCD_EN = 20
  wait(0.1)
  pass

#Btn C: Sleep ON OFF
def buttonC_wasPressed():
  # global params
  global Sleep_EN
  #speaker.tone(646, 120, 1)
  Sleep_EN = 1-Sleep_EN
  wait(0.1)
  pass

PORT_IIC_internal=(21,22)

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x111111)
screen.set_screen_brightness(80)

Path = 'res'
print("OS root file system:")
filesystem = os.listdir()
print(os.listdir())
lcd.print(str(filesystem), 10, 40, 0xFFAAAA)
print("root/res:")
print(os.listdir(Path))
filesystem=os.listdir(Path)
lcd.print("res/"+str(filesystem), 10, 80, 0xFFAAAA)
time.sleep(1)
Sleep_EN = 0
LCD_EN = 75
try:
  #image_BMW = M5Img("res/BMW_coupit BG3.png", x=0, y=0, parent=None)
  #image_BMW.set_hidden(True)
  image_BG = M5Img("res/BG_debug.png", x=0, y=0, parent=None)
  #lcd.image(lcd.CENTER, lcd.CENTER, 'res/ghost_in_the_shell.jpg')
  time.sleep(2) 
except:
  print("load BG image file error")
  pass


#label0 =M5Label('Text', x=54, y=35, color=0x000, font=FONT_MONT_14, parent=None)
#title = M5Title(title="  ESP32 IIC debug v2.1, list iic addresses", x=3 , fgcolor=0xff99aa, bgcolor=0x1F1F1F)
title = M5Label('CoreS3 IIC debug v1.0, list iic addresses', x=2, y=0, color=0xff99aa, font=FONT_MONT_14, parent=None)
#a = i2c_bus.get(i2c_bus.PORTA)
i2c0 = i2c_bus.easyI2C(i2c_bus.PORTA, 0x68, freq=100000)
i2c1 = i2c_bus.easyI2C(PORT_IIC_internal, 0x127, freq=400000)
label_t = M5Label("PortA IIC address list:",x=10, y=20, font=FONT_MONT_14,color=0xF0DFA0)
label1 = M5Label("IIC address list",x=10, y=40, font=FONT_MONT_14,color=0xFFFFAA)

label_info1 = M5Label("iic sacn loop:",x=20, y=200,color=0xDFCF1F,font=FONT_MONT_18)
label_info2 = M5Label("text loop:",x=20, y=220,color=0xDFCF1F,font=FONT_MONT_18)
label_info3 = M5Label("sleep:",x=190, y=225,color=0xDFCF1F,font=FONT_MONT_14)
#label2 = M5TextBox(10, 100, "Text", lcd.FONT_DejaVu24,0xFFAAAA, rotate=0)
image_BG.set_hidden(True)


        #pass#continue

while True:
    #lcd.setBrightness(0)  
    #start = time.ticks_ms() # get millisecond counter
    if btnC.isPressed():
       buttonC_wasPressed()   
    if btnB.isPressed():
       buttonB_wasPressed()
    if btnA.isPressed():
       buttonA_wasPressed()   

    #lcd.setBrightness(LCD_EN)
    screen.set_screen_brightness(LCD_EN)
    start = time.ticks_ms() # get millisecond counter   
    addrList = i2c0.scan()
    delta_IIC = time.ticks_diff(time.ticks_ms(), start) # compute time difference
    print("PORTA IIC(21,22) addrList:")
    print(addrList)
    l=len(addrList)
    label1.set_text(str(addrList))
    #lcd.print("%02x%%" % ((addrList)), 10, 100, COLOR_GREEN)
    lcd.print("0x", 10, 60, 0xFFAAAA)
    #------display in hex format
    for i in range(0, l, 1):
     lcd.print("%x%%" % ((addrList[i])), 35+i*60, 60, 0xFFAAAA)
    lcd.print( "PORTA addr:     ", 10, 80, 0xFFAAFF)
    lcd.print( str(l), 110, 80, 0xFFAACC)
    
    try:
        print("Internal IIC(21,22) addrList:")
        #---------internal iic address--------------------
        #---------[52, 56, 81, 104]-----------------
        #start = time.ticks_ms() # get millisecond counter   
        addrList2 = i2c1.scan()
        #delta_IIC = time.ticks_diff(time.ticks_ms(), start) # compute time 
        print(addrList2)
        l2=len(addrList2)
        #lcd.print("%02x%%" % ((addrList)), 10, 100, COLOR_GREEN)
        lcd.print("0x", 10, 140, 0x3FAAAA)
        #------display in hex format
        for i in range(0, l2, 1):
          lcd.print("%x%%" % ((addrList2[i])), 35+i*60, 140, 0x3FAAAA)
        lcd.print( "Intern addr:     ", 10, 160, 0x3FAAFF)
        lcd.print( str(l2), 110, 160, 0x3FAACC)
    except:
        print('Internal IIC scan error')
        
    #lcd.print( " ".join(hex(ord(n)) for n in addrList),10, 200, COLOR_GREEN)
    #-------------time diff -----------------
    #delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
    label_info1.set_text("IIC scan loop: "+str(delta_IIC)+" ms")  #takes about 2ms
    delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
    label_info2.set_text("text loop: "+str(delta)+" ms")
    start = time.ticks_ms() # get millisecond counter   
    #machine.deepsleep(1000)# put the device to sleep for 1 seconds
    time.sleep_ms(100)
    delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
    label_info3.set_text("sleep: "+str(delta)+" ms")
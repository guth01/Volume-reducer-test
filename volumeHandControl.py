import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

cap=cv2.VideoCapture(0)
wCam,hCam=640,480
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0

detector=htm.handDetector()


device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#print(f"Audio output: {device.FriendlyName}")
#print(f"- Muted: {bool(volume.GetMute())}")
volRange=volume.GetVolumeRange()

minvol=volRange[0]
maxvol=volRange[1]
#print(f"- Volume range: {volume.GetVolumeRange()[0]} dB - {volume.GetVolumeRange()[1]} dB")
vol=0
volBar=400
volPer=0
while True:
    success,img=cap.read()
    detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    if len(lmlist)!=0:

        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)
        #print(length)

        #hand:30-250
        #col:-65:0

        vol=np.interp(length,[30,250],[minvol,maxvol])
        volBar=np.interp(length,[30,250],[400,150])
        volPer=np.interp(length,[30,250],[0,100])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol,None)
        if length <30:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,f':{int(volPer)} %',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.imshow("Img",img)
    cv2.waitKey(1)
import cv2.cv as cv
import time
import os
import sys
from datetime import datetime
from dropbox import client, rest, session
from dropbox.client import DropboxClient
from dropbox.rest import RESTClient
from twilio.rest import TwilioRestClient
from pygame import mixer

#filecounter = 0
# Get your app key and secret from the Dropbox developer website
APP_KEY = '1fvcozry4szbjl4'
APP_SECRET = 'a3v1t9bztccwgoa'
ACCESS_TYPE = 'app_folder'

#One time authorize
TOKENS = 'dropbox_token.txt'
token_file = open(TOKENS)
token_key,token_secret = token_file.read().split('|')
token_secret = token_secret.rstrip('\n')
token_file.close()

#session code
sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
sess.set_token(token_key,token_secret)
client = client.DropboxClient(sess)

#common variables

swf = "swf"
folder = '/home/pi/pictures'
search_dir = folder
os.chdir(search_dir)
files = filter(os.path.isfile, os.listdir(search_dir))
files = [os.path.join(search_dir, f) for f in files] # add path to each file
files.sort(key=lambda x: os.path.getmtime(x))
for deletefile in files:
  if deletefile.endswith(swf):
    os.remove(deletefile)

folder = '/home/pi/pictures/'
search_dir = folder
os.chdir(search_dir)
files = filter(os.path.isfile, os.listdir(search_dir))
files = [os.path.join(search_dir, f) for f in files] # add path to each file
files.sort(key=lambda x: os.path.getmtime(x))
if (len(files) == 0):
  sys.exit()
lastlink =files[-1]
title = lastlink[18:] 
print title
names = title #put name of last file in directory in names
clark = True
class ColorTracker:
  
  def runbrown(self):
    global clark
    #check = True
    #for name in names:
    frame1 = cv.LoadImage(names, 1)
  # while (check == True):
    img = cv.CloneImage(frame1)
    cv.Smooth(img, img, cv.CV_BLUR, 3);
    hsv_img = cv.CreateImage(cv.GetSize(img), 8, 3) 
    cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV)
    thresholded_img =  cv.CreateImage(cv.GetSize(hsv_img), 8, 1) 
    cv.InRangeS(hsv_img, (0,0,250), (182,129,255), thresholded_img) #dark maroon
    #cv.InRangeS(hsv_img,(255,255,255),(255,255,255),thresholded_img) 
    mat = cv.GetMat(thresholded_img)
    moments = cv.Moments(mat)
    moments.m00
    area = cv.GetCentralMoment(moments, 0, 0) 
    if(area > 100000):
      x = cv.GetSpatialMoment(moments, 1, 0)/area
      y = cv.GetSpatialMoment(moments, 0, 1)/area
      overlay = cv.CreateImage(cv.GetSize(img), 8, 3)
      cv.Circle(overlay, (int(x), int(y)), 2, (255, 255, 255), 20)
      cv.Add(img, overlay, img)
      cv.Merge(thresholded_img, None, None, None, img)
      cv.SaveImage("/home/pi/image.jpg",img)
      filestring = "/home/pi/image.jpg"
      print "success"
     # cv.ShowImage('d', img) #display the image, delete to pi later
      c = cv.WaitKey(50)
    else:
      clark = False
    folder = '/home/pi/pictures'
    search_dir = folder
    os.chdir(search_dir)
    files = filter(os.path.isfile, os.listdir(search_dir))
    files = [os.path.join(search_dir, f) for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    for deletefile in files:
      os.remove(deletefile)
    return (0)
			
if __name__ == "__main__":
  storage = cv.CreateMemStorage(0)
  #cv.NamedWindow('d', 1) #delete the d before inserting into pi
  color_tracker = ColorTracker() 
  color_tracker.runbrown()
  #Dropbox Code
  #dropboxfile=open('filetest.jpg')
  if (clark == True):
    dropboxfile=open("/home/pi/image.jpg")
    response = client.put_file("/image.jpg",dropboxfile)
    link=client.share(response["path"])
    final= link['url']
    print final 
   #Twilio Code
    account = "ACebdd9af86ec48d7d29f805de1c0f75ab"
    token = "b637248d7e22ad046a388fa122f7022e"
    client = TwilioRestClient(account, token)
    message = client.sms.messages.create(to="+18327140243", from_="+18324954516",body="alert, home system detected something. livestream: 192.168.1.6:8081" + final) 
#play sound
    mixer.init()
    alert=mixer.Sound('police_s.wav')
    alert.play
    sys.exit()
  else:
    sys.exit()

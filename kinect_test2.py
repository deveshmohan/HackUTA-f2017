import freenect
import cv2
import numpy as np
import select
import sys
from PIL import Image
import time
import argparse
import subprocess
import os


argparser = argparse.ArgumentParser()
argparser.add_argument('-e', '--email', action='store_true')
argparser.add_argument('in_file', type=argparse.FileType("rb"), default=sys.stdin, nargs='?');
args = argparser.parse_args();

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
in_file = args.in_file
last_image = 0;
last_num_faces = 0
firstFrame = None
DEVNULL = open('/dev/null', 'wb')
"""
Grabs a depth map from the Kinect sensor and creates an image from it.
"""

while 1:
	select.select([in_file], [], [])
        rgb = np.fromfile(in_file, dtype=np.uint8, count=640*480*3)
        rgb.shape = (480, 640, 3)
        # sys.stderr.write(repr(rgb))
	gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
	if firstFrame is None:
		firstFrame = cv2.GaussianBlur(gray, (21, 21), 0)
		continue
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	_,cnts,hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        text = "Unoccupied"
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < 1000:
			continue
 
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		# cv2.rectangle(rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"

	faces = faceCascade.detectMultiScale(
    		gray,
    		scaleFactor=1.1,
    		minNeighbors=5,
    		minSize=(30, 30),
    		flags = cv2.CASCADE_SCALE_IMAGE
		)

        now = time.time()

	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
    		cv2.rectangle(rgb, (x, y), (x+w, y+h), (0, 255, 0), 2)

	cv2.putText(rgb, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(rgb, time.strftime("%A %d %B %Y %I:%M:%S%p",time.gmtime(now)), (10, rgb.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        rgb.tofile(sys.stdout)

        if len(faces) > 0:
            if now >= last_image + 60 or len(faces) > last_num_faces:
                last_image = now
                last_num_faces = len(faces)
                image = Image.fromarray(rgb)
                formatted_time = time.strftime('%Y-%m-%d-%H:%M:%S',time.gmtime(now))
                if not os.path.isdir('http/gallery'):
                    os.mkdir('http/gallery')
                image_name = 'http/gallery/{0}.png'.format(formatted_time)
                image.save(image_name)

                subprocess.Popen(["python2", "send_email.py", str(len(faces)), image_name, formatted_time], stdout=DEVNULL);

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
"""
Grabs a depth map from the Kinect sensor and creates an image from it.
"""

while 1:
	select.select([in_file], [], [])
        rgb = np.fromfile(in_file, dtype=np.uint8, count=640*480*3)
        rgb.shape = (480, 640, 3)
        # sys.stderr.write(repr(rgb))
	gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
    		gray,
    		scaleFactor=1.1,
    		minNeighbors=5,
    		minSize=(30, 30),
    		flags = cv2.CASCADE_SCALE_IMAGE
		)
	# print "Found {0} faces!".format(len(faces))

	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
    		cv2.rectangle(rgb, (x, y), (x+w, y+h), (0, 255, 0), 2)
        rgb.tofile(sys.stdout)

        if faces:
            now = time.time();
            if now >= last_image + 60 or len(faces) > last_num_faces:
                last_image = now
                last_num_faces = len(faces)
                image = Image.fromarray(rgb, now)
                formatted_time = time.strftime('%Y-%m-%d-%H:%M:%S',time.gmtime(now))
                if not os.path.isdir('http/gallery'):
                    os.mkdir('http/gallery')
                image_name = 'http/gallery/{0}.png'.format(formatted_time)
                image.save(image_name)

                subprocess.Popen(["python2", "send_email.py", str(num_faces), image_name, formatted_time]);

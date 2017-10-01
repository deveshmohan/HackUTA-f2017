#import cv2
#import freenect

#capture = cv2.VideoCapture(freenect.sync_get_video())
#capture.set(cv2.CAP_OPENNI_IMAGE_GENERATOR_OUTPUT_MODE, cv2.CAP_OPENNI_VGA_30HZ)

#print capture.get(cv2.CAP_PROP_OPENNI_REGISTRATION)

#while True:
#    if not capture.grab():
#        print "Unable to Grab Frames from camera"
#        break
#    okay1, depth_map = capture.retrieve(cv2.CAP_OPENNI_DEPTH_MAP)
#    if not okay1:
#        print "Unable to Retrieve Disparity Map from camera"
#        break
#    okay2, gray_image = capture.retrieve(cv2.CAP_OPENNI_GRAY_IMAGE)
#    if not okay2:
#        print "Unable to retrieve Gray Image from device"
#        break
#    cv2.imshow("depth camera", depth_map)
#    cv2.imshow("rgb camera", gray_image)
#    if cv2.waitKey(10) == 27:
#        break

#freenect.runloop(
#cv2.destroyAllWindows()
#capture.release()

import freenect
import cv2
import numpy as np
import select
import sys

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
in_file = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
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

#	for (x,y,w,h) in faces:
#    		img = cv2.rectangle(rgb,(x,y),(x+w,y+h),(255,0,0),2)
#    		roi_gray = gray[y:y+h, x:x+w]
#    		roi_color = img[y:y+h, x:x+w]
#    		eyes = eye_cascade.detectMultiScale(roi_gray)
#    		for (ex,ey,ew,eh) in eyes:
#        		cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
#        # quit program when 'esc' key is pressed
#        k = cv2.waitKey(5) & 0xFF
#        if k == 27:
#            break
#    	cv2.destroyAllWindows()

#	print faces
#	blur = cv2.GaussianBlur(depth, (5, 5), 0)
# 	blur2 = cv2.GaussianBlur(rgb, (5, 5), 0)
#	cv2.imshow('image', faces)
#	cv2.imshow('image2', rgb)
#	cv2.waitKey(10)

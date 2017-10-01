import argparse
import datetime
import time
import freenect
import cv2
import numpy as np
faceCascade = cv2.CascadeClassifier
firstFrame = None
#('haarcascade_frontalface_default.xml')
"""
Grabs a depth map from the Kinect sensor and creates an image from it.
"""
def getDepthMap():	
	depth, timestamp = freenect.sync_get_depth()
 
	np.clip(depth, 0, 2**10 - 1, depth)
	depth >>= 2
	depth = depth.astype(np.uint8)
 
	return depth
def getRGB():	
	rgb, timestamp = freenect.sync_get_video()
	#rgb = (rgb * 258).round().astype(np.uint8)
 	rgb = rgb.astype(np.uint8)
	return rgb
while True:
	
#	eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
	depth = getDepthMap()
 	rgb = getRGB()
	#print repr(rgb)
	frame = rgb
	#print repr(frame)
	text="Unoccupied"	
	print firstFrame
	gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	if firstFrame is None:
		firstFrame = gray
		continue
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
#	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
#		cv2.CHAIN_APPROX_SIMPLE)
#	im_ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)
#	skin_ycrcb_mint = np.array((0, 133, 77))
#	skin_ycrcb_maxt = np.array((255, 173, 127))
#	skin_ycrcb = cv2.inRange(im_ycrcb, skin_ycrcb_mint, skin_ycrcb_maxt)
	_,cnts,hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#	(_, cnts, _) = cv2.findContours(skin_ycrcb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < 1000:
			continue
 
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
cv2.destroyAllWindows()




	#print gray
#	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#	faces = faceCascade.detectMultiScale(
#    		gray,
#    		scaleFactor=1.1,
#    		minNeighbors=5,
#    		minSize=(30, 30),
#    		flags = cv2.CASCADE_SCALE_IMAGE
#		)
#	print "Found {0} faces!".format(len(faces))

#	# Draw a rectangle around the faces
#	for (x, y, w, h) in faces:
#    		cv2.rectangle(rgb, (x, y), (x+w, y+h), (0, 255, 0), 2)
#	cv2.imshow("Faces found" ,rgb)
#	cv2.waitKey(1)






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

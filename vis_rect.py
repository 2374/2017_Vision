# refer to http://opencv-python-tutroals.readthedocs.io/en/latest/index.html for documentation of OpenCV

import numpy as np
import cv2
from networktables import NetworkTable

def sendData(contours):
	xList = []
	yList = []
	wList = []
	hList = []
	
	for cnt in contours:
		x,y,w,h = cnt
		xList.append(x)
		yList.append(y)
		wList.append(w)
		hList.append(h)
	
	table = NetworkTable.getTable("vision")
	table.putNumberArray("x", xList)
	table.putNumberArray("y", yList)
	table.putNumberArray("w", wList)
	table.putNumberArray("h", hList)
	return
	
def processImage(img):
	# convert BGR to HSV
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	
	# threshold to only include wanted HSV values
	thresh = cv2.inRange(hsv,np.array(hsv_lower_bound),np.array(hsv_upper_bound))
	
	return thresh

def getPreferedContours(img):
	# using contours to form shapes
	image, contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	
	# output array
	output = []
	
	# sorting through all the countours
	for cnt in contours:
	
		#the area of the countour
		area = cv2.contourArea(cnt)

		# filtering out contours that are too big or too small
		if area_min < area:
			
			# creating a rectangle the contour
			x,y,w,h = cv2.boundingRect(cnt)
			
			output.append([x,y,w,h])

	return output
	
if __name__ == '__main__':
	# ---preferences--- 
	debugging = True
	networktable_ip = "172.22.11.2"
	hsv_lower_bound = [60,186,41]
	hsv_upper_bound = [92,255,199]
	area_min = 100

	# setup NetworkTables
	NetworkTable.setIPAddress(networktable_ip)
	NetworkTable.setClientMode()
	NetworkTable.initialize()

	# setup camera feed
	cap = cv2.VideoCapture(0)
	cap.set(3,640)
	cap.set(4,480)

	while True:
		# isValid returns if frame is read correctly and frame is a matrix of info from a frame of the camera
		isValid, raw = cap.read()
		
		# process the image
		processed = processImage(raw)
		
		# find the right contours
		contours = getPreferedContours(processed)
		
		sendData(contours)
				
		# drawing a visual box to the debug images
		if debugging:
			for cnt in contours:
				x,y,w,h = cnt
				cv2.rectangle(raw,(x,y),(x+w,y+h),(0,255,0),2)
				cv2.rectangle(processed,(x,y),(x+w,y+h),(0,255,0),2)

		# showing the debug images
		if debugging:
			cv2.imshow('raw',raw)
			cv2.imshow('processed',processed)

			# the amount of milliseconds to wait before the next frame and exits on pressing the esc key
			if cv2.waitKey(5) & 0xFF == 27:
				break

	# when finished, release the capture and destory any created windows 
	cap.release()
	cv2.destroyAllWindows()

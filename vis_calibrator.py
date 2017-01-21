import cv2
import numpy as np


cap = cv2.VideoCapture(0)

def nothing(x):
	pass
# Creating a window for later use
cv2.namedWindow('result')
cv2.namedWindow('output')

# Starting with 100's to prevent error while masking
h_min,s_min,v_min,h_max,s_max,v_max = 0,0,0,0,0,0
area_min,area_max = 0,0

# Creating track bar
cv2.createTrackbar('h min','result',0,180,nothing)
cv2.createTrackbar('s min','result',0,255,nothing)
cv2.createTrackbar('v min','result',0,255,nothing)
cv2.createTrackbar('h max','result',180,180,nothing)
cv2.createTrackbar('s max','result',255,255,nothing)
cv2.createTrackbar('v max','result',255,255,nothing)
cv2.createTrackbar('v max','result',255,255,nothing)
cv2.createTrackbar('area min','result',0,10000,nothing)
cv2.createTrackbar('area max','result',10000,10000,nothing)
cv2.createTrackbar('width min','result',0,320,nothing)
cv2.createTrackbar('width max','result',320,320,nothing)
cv2.createTrackbar('height min','result',0,240,nothing)
cv2.createTrackbar('height max','result',240,240,nothing)

while(1):

	_, frame = cap.read()
	cap.set(3,640)
	cap.set(4,480)

	# converting to HSV
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

	# get info from track bar and apply to result
	h_min = cv2.getTrackbarPos('h min','result')
	s_min = cv2.getTrackbarPos('s min','result')
	v_min = cv2.getTrackbarPos('v min','result')
	h_max = cv2.getTrackbarPos('h max','result')
	s_max = cv2.getTrackbarPos('s max','result')
	v_max = cv2.getTrackbarPos('v max','result')
	area_min = cv2.getTrackbarPos('area min','result')
	area_max = cv2.getTrackbarPos('area max','result')
	width_min = cv2.getTrackbarPos('width min','result')
	width_max = cv2.getTrackbarPos('width max','result')
	height_min = cv2.getTrackbarPos('height min','result')
	height_max = cv2.getTrackbarPos('height max','result')

	# hsv masking
	lower_range = [h_min,s_min,v_min]
	upper_range = [h_max,s_max,v_max]

	mask = cv2.inRange(hsv,np.array(lower_range),np.array(upper_range))

	result = cv2.bitwise_and(frame,frame,mask = mask)

	image,contours,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

	for cnt in contours:
		area = cv2.contourArea(cnt)
		if area_min < area < area_max:

			# used for circles
			#(x,y),radius = cv2.minEnclosingCircle(hull)
			#center = (int(x),int(y))
			#radius = int(radius)
			#cv2.circle(result,center,radius,(0,255,0),2)

			# used for rectangles
			x,y,w,h = cv2.boundingRect(cnt)
			if width_min < w < width_max and height_min < h < height_max:
				cv2.rectangle(result,(x,y),(x+w,y+h),(0,255,0),2)

	cv2.imshow('output',result)
	cv2.imshow('hsv', mask)

	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cap.release()

cv2.destroyAllWindows()

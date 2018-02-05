import cv2
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl


CONTRAST_THRESHOLD = 80
HISTOGRAM_SIZE = 256
mini = 0
maxi = 255
diff = 255
histogram = np.zeros(HISTOGRAM_SIZE, dtype = np.uint)
capture = cv2.VideoCapture(0)

while(capture.isOpened()):
	ret, frame = capture.read()
	height, width, channels = frame.shape
	print(height, width)
	gray_image = np.zeros([height,width], dtype=np.uint8)

	for i in range(0,height):
		for j in range(0,width):
			gray_image[i,j] = np.uint8(0.3*frame[i,j,2] + 0.59*frame[i,j,1] + 0.11*frame[i,j,0])	# B,G,R
			histogram[gray_image[i,j]] = histogram[gray_image[i,j]] + 1
			if(gray_image[i,j] < mini):
				gray_image[i,j] = 0
			elif(gray_image[i,j] > maxi):
				gray_image[i,j] = 255
			else: #if(gray_image[i,j] >= mini and gray_image[i,j] <= maxi):
				gray_image[i,j] = np.uint8((maxi*(gray_image[i,j]-mini)/diff))

	x = 0
	while(x < HISTOGRAM_SIZE and histogram[x] < CONTRAST_THRESHOLD):
		x = x + 1
	mini = x
	x = HISTOGRAM_SIZE - 1
	while(x > mini and histogram[x] < CONTRAST_THRESHOLD):
		x = x - 1
	maxi = x
	diff = maxi - mini
	print(diff)
	#pl.imshow(gray_image)
	#pl.pause(0.00001)
	#pl.draw()
	#gray_image = gray_image/256 #normalising - only for cv2.imshow(), if pl.draw() is used, this is not needed
	cv2.imshow('frame',gray_image)
	
	if cv2.waitKey(1) & 0xFF == 27 :
		break

capture.release()
cv2.destroyAllWindows()
import cv2
import numpy as np

CONTRAST_THRESHOLD = 80
HISTOGRAM_SIZE = 256
mini = 0
maxi = 255
diff = 255
capture = cv2.VideoCapture(0)


#Generaltesting - nothing to do with program
#arr = np.zeros(5, dtype = np.uint)
#arr[0] = 50
#arr[1] = 60
#arr[2] = 70
#arr[3] = 80
#arr[4] = 90
#print(arr)
#temp = np.where((arr > 55)&(arr<85))
#arr[temp] = arr[temp]-10
#print(arr)
#arr[temp] = arr[temp]*4
#print(arr)
#arr[temp] = arr[temp]/2
#print(arr)

while(capture.isOpened()):
	ret, frame = capture.read()
	height, width, channels = frame.shape
	gray_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

	#gray_image[np.where(gray_image < mini)] = 0
	#gray_image[np.where(gray_image > maxi)] = 255

	# Perhaps a more elegant and (slightly) faster way for contrast enhancement, but currently does not work: upper half of frame black
	#temp_indices = gray_image[np.where((gray_image >= mini)&(gray_image <= maxi))]
	#gray_image[temp_indices] = gray_image[temp_indices] - mini	
	#gray_image[temp_indices] = gray_image[temp_indices] * 255
	#gray_image[temp_indices] = gray_image[temp_indices]/diff

	for i in range(0,height):
		for j in range(0,width):
			if(gray_image[i,j] > maxi):
				gray_image[i,j] = 255
			elif(gray_image[i,j] < mini):
				gray_image[i,j] = 0
			else:#if(gray_image[i,j] >= mini and gray_image[i,j] <= maxi):
				gray_image[i,j] = np.uint8(255*(gray_image[i,j]-mini)/diff)

	hist = cv2.calcHist([gray_image],[0],None,[256],[0,256])
	mini = np.where(hist >= CONTRAST_THRESHOLD)[0][0]
	if mini > 0 :
		mini = mini - 1
	hist_rev = hist[::-1]
	hist_rev = hist_rev[:(256-mini)]
	maxi = np.where(hist_rev >= CONTRAST_THRESHOLD)[0][0]
	maxi = 255 - maxi
	if maxi < HISTOGRAM_SIZE:
		maxi = maxi + 1
	diff = maxi - mini
	
	cv2.imshow('frame',gray_image)

	if cv2.waitKey(1) & 0xFF == 27 :
		break

capture.release()
cv2.destroyAllWindows()
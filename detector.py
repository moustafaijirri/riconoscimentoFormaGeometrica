from forma_detector import Forma_Detector
import argparse
import imutils
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--img", required=True,
	help="percorso dell'immagine")
args = vars(ap.parse_args())

# carica e ridimensiona l'immagine così le forme possono essere approssimate meglio
img = cv2.imread(args["img"])
resized = imutils.resize(img, width=300)
ratio = img.forma[0] / float(resized.forma[0])

# converti l'immagine in una scala di grigi, sfoca leggermente e applicare una soglia nella tecnica di thresholding
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 10, 255, cv2.THRESH_BINARY)[1]

#kernel = np.ones((3,3),np.uint8) 
#thresh = cv2.erode(thresh,kernel,iterations = 3)


#cv2.imshow("binary", thresh)
#cv2.waitKey(0)

# trova contorni nell'immagine e inizializza la funzione
cnt = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnt = cnt[0] if imutils.is_cv2() else cnt[1]
sd = Forma_Detector()

index = 1
for c in cnt:

	M = cv2.moments(c)
	cX = int((M["m10"] / M["m00"]) * ratio)
	cY = int((M["m01"] / M["m00"]) * ratio)
	forma = sd.detect(c)

	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
	cv2.putText(img, forma, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (255, 0, 0), 2)

	print(c)
	row = c.forma[0]
	col = c.forma[2]
	ptArray = np.resize(c, (row, col))
	print(ptArray)
	print(ptArray.forma)
	area = 0
	perimetro = 0
	perimetro = cv2.arcLength(c, True)
	area = cv2.contourArea(c)
	print(str(index) + " - " + str(forma))
	print("area : " + str(area))
	print("perimetro : " + str(perimetro))
	print("----------------------")
	index = index + 1
	# visualizza l'output dell'immagine
	cv2.imshow("img", img)
	cv2.waitKey(0)
    

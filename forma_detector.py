import cv2

class Forma_Detector:
	def __init__(self):
		pass

	def detect(self, c):
		# inizializza il nome della forma e approssima il contorno
		forma = "non definito"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)

		# se la forma è un triangono, avrà 3 vertici
		if len(approx) == 3:
			forma = "triangolo"

		# se la forma ha 4 vertici, è un quadrato o
		# un rettangolo
		elif len(approx) == 4:
			# calcola il contorno del rettangolo circoscritto e la proporzione
			(x, y, w, h) = cv2.boundingRect(approx)
			pr = w / float(h)

			# un quadrato ha una proporzione approssimata a uno, altrimenti la forma è un rettangolo
			forma = "quadrato" if pr >= 0.95 and pr <= 1.05 else "rettangolo"

		# se la forma è un pentagono, avrà 5 vertici
		elif len(approx) == 5:
			forma = "pentagono"

		# altrimenti la forma è un cerchio
		else:
			forma = "cerchio"

		# return del nome della forma
		return forma
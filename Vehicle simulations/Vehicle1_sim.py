import numpy as np
import cv2
from Field import Field
from Vehicle import *

if __name__=='__main__':
	background = Field((1000,1000),np.random.randint(100,900,size=(20,2)),2)
	# background.display_field()

	V1 = Vehicle_1sensor(center = (500,500), orientation = np.pi/3, height = 50, width = 30, K = 10, noise_sigma = 7)

	while True:
		img = background.img.copy()
		img = V1.draw(img)
		cv2.imshow("Vehicle",img)
		if cv2.waitKey(50)==27:
			break
		V1.state_update(background)
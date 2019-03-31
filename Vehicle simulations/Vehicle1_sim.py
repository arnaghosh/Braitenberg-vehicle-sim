import numpy as np
import cv2
from Field import Field
from Vehicle import *

if __name__=='__main__':
	background = Field((1000,1000),np.random.randint(100,900,size=(30,2)),3)
	# background.display_field()

	V1 = Vehicle_1sensor(center = (500,500), orientation = np.pi/3, height = 50, width = 30, K = 10, noise_sigma = 7)

	# fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
	# out = cv2.VideoWriter('output.avi',fourcc, 33.0, (1000,1000))

	while True:
		img = background.img.copy()
		img = V1.draw(img)
		cv2.imshow("Vehicle",img)
		# out.write(np.uint8(np.clip(225*img,0,255)))
		if cv2.waitKey(33)==27:
			break
		V1.state_update(background)

	cv2.destroyAllWindows()
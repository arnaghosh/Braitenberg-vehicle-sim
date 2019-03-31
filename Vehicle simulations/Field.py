import cv2
import numpy as np

class Field():
	def __init__(self,size, sources,field_order):
		# Setup a field, create an image with zeros and populate intensity values with field strength values 
		# sources - Set of coord of sources
		# field_order - Order of field strength decay from a single source
		self.img = np.zeros(np.array(size+(3,)))
		self.field_order = field_order
		self.create_field(sources)

	def radial_pattern(self, pt_x, pt_y):
		# creates a field strength pattern for one source
		height = self.img.shape[0]
		width = self.img.shape[1]
		row_arr = np.array([np.linspace(0,height-1,height)]*width).T
		col_arr = np.array([np.linspace(0,width-1,width)]*height)
		row_arr = abs(row_arr-pt_y)
		col_arr = abs(col_arr-pt_x)
		radial_pattern_arr = 1+np.power(np.power(row_arr,self.field_order)+np.power(col_arr,self.field_order),1./self.field_order)
		radial_pattern_arr = 3./radial_pattern_arr
		return np.repeat(radial_pattern_arr[:,:,np.newaxis],3,axis=2)

	def create_field(self, sources):
		# creates additive field strength pattern of all sources
		for s in range(len(sources)):
			self.img = self.img + self.radial_pattern(sources[s,0],sources[s,1])

	def display_field(self):
		# display the field strength as an image
		cv2.imshow("Field",self.img)
		cv2.waitKey(0)


if __name__ =='__main__':
	# Testing functions and how to initiate Field object example
	background = Field((200,200),np.random.randint(20,180,size=(10,2)),2)
	background.display_field()
	
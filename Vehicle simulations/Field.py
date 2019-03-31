import turtle
import cv2
import numpy as np

class Field():
	def __init__(self,size, sources,field_order):
		self.img = np.zeros(np.array(size+(3,)))
		self.field_order = field_order
		self.create_field(sources)
		# print(self.img)

	def radial_pattern(self, pt_x, pt_y):
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
		for s in range(len(sources)):
			self.img = self.img + self.radial_pattern(sources[s,0],sources[s,1])

	def display_field(self):
		cv2.imshow("Field",self.img)
		cv2.waitKey(0)


if __name__ =='__main__':
	background = Field((200,200),np.random.randint(20,180,size=(10,2)),2)
	background.display_field()
	
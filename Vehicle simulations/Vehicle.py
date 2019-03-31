import numpy as np
import cv2


def add_vector(pt, distance, direction):
	# a generic function for adding a displacement vector to a pt and obtain a new pt
	new_pt = (int(round(pt[0]+distance*np.cos(direction))),int(round(pt[1]-distance*np.sin(direction))))
	return new_pt

class Vehicle():
	# generic vehicle class
	def __init__(self, center, orientation, height, width):
		# defines generic properties like initial center pos, initial orientation and dimensions of bot
		# the color combination is fixed as of now but can be changed later
		# calculates the head and tal pos from initial center and orientation information
		self.center = center
		self.orientation = orientation
		self.vehicle_ht = height
		self.vehicle_wd = width
		self.body_color = (0,0,1)	# red colored body
		self.sensor_color = (0,1,1)	# yellow colored sensor
		self.motor_color = (0,1,0)	# green colored motor/wheel
		self.sensor_motor_radius = 7
		self.velocity = 0
		self.omega = 0
		self.head_pos = add_vector(self.center,self.vehicle_ht/2,self.orientation)
		self.tail_pos = add_vector(self.center, self.vehicle_ht/2,self.orientation+np.pi)

	def state_update(self):
		# update center pos, head pos, tail pos and orientation depending on velocity and omega
		self.center = add_vector(self.center,self.velocity,self.orientation)
		self.orientation = self.orientation + self.omega
		self.head_pos = add_vector(self.center,self.vehicle_ht/2,self.orientation)
		self.tail_pos = add_vector(self.center, self.vehicle_ht/2,self.orientation+np.pi)

	def set_velocity(self,velocity):
		# updates velocity
		self.velocity = velocity

	def set_omega(self,omega):
		# updates omega (angluar velocity)
		self.omega = omega

class Vehicle_1sensor(Vehicle):
	# Vehicle type 1 class
	def __init__(self, center, orientation, height, width, K, noise_sigma = 0):
		# puts a sensor in the head pos and a motor in the tail pos
		# also defines the sensor gain and randomness in omega
		Vehicle.__init__(self, center, orientation, height, width)
		self.motor_pos = self.tail_pos
		self.sensor_pos = self.head_pos
		self.sensor_to_motor_gain = K
		self.omega_noise_std = noise_sigma*np.pi/180

	def state_update(self, Field = None):
		# take sensor observation and update velocity and omega values
		# if no field strength is passes, assume free space (no change)
		if Field != None:
			observation = Field.img[self.sensor_pos[1]%Field.img.shape[1],self.sensor_pos[0]%Field.img.shape[0],0]
			self.set_velocity(self.sensor_to_motor_gain*observation)
			self.set_omega(np.random.normal(0,self.omega_noise_std))
		Vehicle.state_update(self)
		self.motor_pos = self.tail_pos
		self.sensor_pos = self.head_pos		

	def draw(self, img):
		# draws the vehicle on a canvas (img)
		# calculates the 4 vertices of the vehicle to create a polygon
		top_left = add_vector(self.head_pos,self.vehicle_wd/2,np.pi/2+self.orientation)
		top_right = add_vector(self.head_pos,self.vehicle_wd/2,3*np.pi/2+self.orientation)
		bottom_left = add_vector(self.tail_pos,self.vehicle_wd/2,np.pi/2+self.orientation)
		bottom_right = add_vector(self.tail_pos,self.vehicle_wd/2,3*np.pi/2+self.orientation)
		vehicle_pts = np.array([top_left,bottom_left,bottom_right,top_right], dtype=np.int32)
		vehicle_pts.reshape((-1,1,2))

		cv2.fillConvexPoly(img,vehicle_pts,self.body_color)	# draw the vehicle as a closed polygon
		cv2.circle(img,self.sensor_pos,self.sensor_motor_radius,self.sensor_color,-1)	# draw the sensor as a circle
		cv2.circle(img,self.motor_pos,self.sensor_motor_radius,self.motor_color,-1)		# draw the motor as a circle
		return img


if __name__ =='__main__':
	# Testing functions and example for initiating objects
	V1 = Vehicle_1sensor(center = (250,250), orientation = np.pi/3, height = 50, width = 30, K = 10)
	background = np.zeros((500,500,3))
	# V1.set_omega(2*np.pi/180)
	V1.set_velocity(2)
	while True:
		img = background.copy()
		img = V1.draw(img)
		cv2.imshow("Vehicle",img)
		if cv2.waitKey(50)==27:
			break
		V1.state_update()

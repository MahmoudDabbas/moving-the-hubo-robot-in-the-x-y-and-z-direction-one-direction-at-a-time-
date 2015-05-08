#!/usr/bin/env python
import pygame
import time
import math
from numpy  import *
from numpy.linalg import *
pygame.init()
# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Current position
x_coord = 10
y_coord = 10
joystick_count = pygame.joystick.get_count()

import hubo_ach as ha
import ach
import sys
import time
from ctypes import *

while joystick_count == 0:
# No joysticks!
    	print("Error, I didn't find any joysticks.")
else :
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()
    print "got joystick!!!!!!!!!!!!!!!"
alpha=-3.1415/6
beta=-3.1415/2
gamma=0
while not done:
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                    done = True

	        # This gets the position of the axis on the game 	controller	
        # It returns a number between -1.0 and +1.0
	x = my_joystick.get_axis(0)
	print "x = : ",x	
	y = my_joystick.get_axis(1)
	#jl10 = my_joystick.get_axis(2)
	z = my_joystick.get_axis(2)




	# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
	s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
	r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
	#s.flush()
	#r.flush()
	
	# feed-forward will now be refered to as "state"
	state = ha.HUBO_STATE()
	
	# feed-back will now be refered to as "ref"
	ref = ha.HUBO_REF()
	
	# Get the current feed-forward (state) 
	[statuss, framesizes] = s.get(state, wait=False, last=False)
	
	#Set Left Elbow Bend (LEB) and Right Shoulder Pitch (RSP) to  -0.2 rad and 0.1 rad respectively

	a00= 0
	a01= 0.18*math.cos(beta)*math.cos(gamma)
	a02= -0.18*math.sin(beta)*math.sin(gamma)

	a10=0.18*(-math.sin(alpha)*(1+math.cos(beta))+math.sin(beta)*math.cos(alpha)*math.sin(gamma))
	a11=0.18*(-math.cos(alpha)*math.sin(beta)+math.cos(beta)*math.sin(alpha)*math.sin(gamma))
	a12=0.18*math.sin(beta)*math.sin(alpha)*math.cos(gamma)
	
	a20= 0.18*(-math.cos(alpha)*(1+math.cos(beta))-math.sin(beta)*math.sin(alpha)*math.sin(gamma))
	a21= 0.18*(+math.sin(alpha)*math.sin(beta)+math.cos(beta)*math.cos(alpha)*math.sin(gamma))
	a22=+0.18*math.sin(beta)*math.cos(alpha)*math.cos(gamma)


	matrix = array([[a00,a01,a02],[a10,a11,a12],[a20,a21,a22]])
	#print matrix
	inverse= inv(matrix)
	print "invers is = "
	print inverse
	x1=0.18*math.sin(beta)*math.cos(gamma)
	y1=0.18*(math.cos(alpha)*(1+math.cos(beta))+math.sin(beta)*math.sin(alpha)*math.sin(gamma))
	z1=0.18*(-math.sin(alpha)*(1+math.cos(beta))+math.sin(beta)*math.cos(alpha)*math.sin(gamma))
	print "x equals = ",x1
	print "y equals = ",y1
	print "z equals = ",z1

	if x>0.0:
		alpha = alpha + .002*inverse[0][0]
		beta = beta + .002*inverse[1][0]
		gamma = gamma + .002*inverse[2][0]
	if x<0.0:	
		alpha = alpha - .002*inverse[0][0]
		beta = beta - .002*inverse[1][0]
		gamma = gamma - .002*inverse[2][0]

	if y>0.0:	
		alpha = alpha + .002*inverse[0][1]
		beta = beta + .002*inverse[1][1]
		gamma = gamma + .002*inverse[2][1]
	if y<0.0:	
		alpha = alpha - .002*inverse[0][1]
		beta = beta - .002*inverse[1][1]
		gamma = gamma - .002*inverse[2][1]

	if z>0.0:	
		alpha = alpha + .002*inverse[0][2]
		beta = beta + .002*inverse[1][2]
		gamma = gamma + .002*inverse[2][2]
	if z<0.0:	
		alpha = alpha - .002*inverse[0][2]
		beta = beta - .002*inverse[1][2]
		gamma = gamma - .002*inverse[2][2]

	#theta= 90*3.1415/180
#	print "theta now is : ", (180/3.1415)*theta 	
	ref.ref[ha.RSY] = gamma
#	ref.ref[ha.RSY] = -3.1415/2
	print "ref.ref[ha.RSY] Gamma = ", (180/3.1415)*gamma
	ref.ref[ha.RSR] = alpha
#	ref.ref[ha.RSR] = -(theta)
	print "ref.ref[ha.RSR] is = Alpha " , (180/3.1415)*ref.ref[ha.RSR]
	ref.ref[ha.REB] = beta
#	ref.ref[ha.REB] = -(3.1415-2*theta)
	print "ref.ref[ha.REB] BETA is = " , (180/3.1415)*ref.ref[ha.REB]
	
	
	#ref.ref[ha.RSP] = 1
	#ref.ref[ha.RSP] = 1

	# Print out the actual position of the LEB
	print "Joint = ", state.joint[ha.LEB].pos

	# Print out the Left foot torque in X
	print "Mx = ", state.ft[ha.HUBO_FT_L_FOOT].m_x

	# Write to the feed-forward channel
	r.put(ref)
	
	# Close the connection to the channels
	r.close()
	s.close()
	time.sleep(.1)

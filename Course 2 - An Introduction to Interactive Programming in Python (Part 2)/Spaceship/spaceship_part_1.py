
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

#import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
TEXT_SIZE=20
score = 0
lives = 3
time = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.ogg")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.ogg")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
	def __init__(self, pos, vel, angle, image, info):
		self.pos = [pos[0],pos[1]]
		self.vel = [vel[0],vel[1]]
		self.angle = angle
		self.angle_vel = 0
		self.image = image
		self.image_center = info.get_center()
		self.image_size = info.get_size()
		self.radius = info.get_radius()
		
		# Ship thrust
		self.thrust = False
		self.friction=0.01
		self.acceleration=0
		
	def draw(self,canvas):
		# Draw a ship with and without trust and play thrust sound
		if(self.thrust == False):
			canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
			ship_thrust_sound.rewind()

		if(self.thrust == True):
			canvas.draw_image(self.image, [ self.image_center[0]+90,self.image_center[1] ], self.image_size, self.pos, self.image_size, self.angle)
			ship_thrust_sound.play()
	
	def ship_spin(self, angle_velocity):
		# Spin the ship at certain velocity
		self.angle_vel = angle_velocity
		
	def ship_trust(self, thrust, acc):
		# Sets ships thrust to T/F and updates acceleration correspondly
		self.thrust=thrust
		self.acceleration = acc
		
	def ship_position(self):
		# Return ship coordinates and angle
		return self.pos[0], self.pos[1], self.angle
		
	def update(self):
		# Motion 
		self.angle += self.angle_vel 
		self.pos[0] += self.vel[0] 
		self.pos[1] += self.vel[1] 
		
		# Wall
		if(self.pos[0] < 0):
			self.pos[0] = WIDTH - self.pos[0]
		elif(self.pos[1] < 0):	
			self.pos[1] = HEIGHT - self.pos[1]

		elif(self.pos[0] > WIDTH):
			self.pos[0] = self.pos[0] - WIDTH
			
		elif(self.pos[1] > HEIGHT):
			self.pos[1] = self.pos[1] - HEIGHT	
		
		# Moving ship
		if self.thrust:
			# Thrust update
			forward = [math.cos(self.angle), math.sin(self.angle)]
			self.vel[0] = forward[0] * self.acceleration
			self.vel[1] = forward[1] * self.acceleration
		else:
			# Friction update
			self.vel[0] *= (1-self.friction)
			self.vel[1] *= (1-self.friction)
			
# Sprite class
class Sprite():
	def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
		self.pos = [pos[0],pos[1]]
		self.vel = [vel[0],vel[1]]
		self.angle = ang
		self.angle_vel = ang_vel
		self.image = image
		self.image_center = info.get_center()
		self.image_size = info.get_size()
		self.radius = info.get_radius()
		self.lifespan = info.get_lifespan()
		self.animated = info.get_animated()
		self.age = 0
		
		self.show_missle = False
				
		if sound:
			sound.rewind()
			sound.play()

	def draw(self, canvas):
		# Draw a missle and a rock on the screen
		if(self.image == missile_image and self.show_missle==True):
			canvas.draw_image(self.image, self.image_center, self.image_size, 
			[ self.pos[0]+angle_to_vector(self.angle)[0]*45, self.pos[1]+angle_to_vector(self.angle)[1]*45 ], 
			self.image_size, self.angle)

		elif(self.image == asteroid_image):
			canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

	def shoot_missle(self, xcord, ycord, ang):
		# Shoots a missle from ships current posistion and angle. Play missle sound		
		self.show_missle=True
		missile_sound.play()
		
		self.angle = ang
		forward = [math.cos(self.angle), math.sin(self.angle)]
		
		self.pos[0] = xcord
		self.pos[1] = ycord
		
		self.vel[0] = forward[0] * 5
		self.vel[1] = forward[1] * 5
		
	def rock_spawn(self):
		# Spawns a rock with random velocity, posistion and angle velocity
		self.pos = [ WIDTH * random.random(), HEIGHT * random.random() ]		
		self.vel = [ uniform( -random.random(), random.random() ) , uniform( -random.random(), random.random() ) ]
		self.angle = uniform(-2*math.pi, 2*math.pi) 
		self.angle_vel = uniform(-0.1,0.1) 
		
	def update(self):
		# Motion sprite
		self.angle += self.angle_vel
		self.pos[0] += self.vel[0]
		self.pos[1] += self.vel[1]
		
		# Wall sprite
		if(self.pos[0] < 0):
			self.pos[0] = WIDTH - self.pos[0]
		elif(self.pos[1] < 0):
			self.pos[1] = HEIGHT - self.pos[1]

		elif(self.pos[0] > WIDTH):
			self.pos[0] = self.pos[0] - WIDTH
			
		elif(self.pos[1] > HEIGHT):
			self.pos[1] = self.pos[1] - HEIGHT

# define keyhandlers to control firing_angle
def keydown(key):
	global my_ship
	if simplegui.KEY_MAP["space"] == key:
		ship_missle.shoot_missle( my_ship.ship_position()[0], my_ship.ship_position()[1], my_ship.ship_position()[2] )
		
	elif simplegui.KEY_MAP["up"] == key:
		acceleration=3
		my_ship.ship_trust(True, acceleration)
		
	elif simplegui.KEY_MAP["left"] == key:
		angle_velocity = -0.05
		my_ship.ship_spin(angle_velocity)
		
	elif simplegui.KEY_MAP["right"] == key:
		angle_velocity = 0.05
		my_ship.ship_spin(angle_velocity)

def keyup(key):
	global my_ship
	if simplegui.KEY_MAP["up"] == key:
		acceleration=0
		my_ship.ship_trust(False, acceleration)
	
	elif simplegui.KEY_MAP["left"] == key:
		angle_velocity = 0
		my_ship.ship_spin(angle_velocity)
	
	elif simplegui.KEY_MAP["right"] == key:
		angle_velocity = 0
		my_ship.ship_spin(angle_velocity)

def draw(canvas):
	global time

	# animiate background
	time += 1
	wtime = (time / 4) % WIDTH
	center = debris_info.get_center()
	size = debris_info.get_size()
	canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
	canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
	canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
	
	# Draw score and life
	canvas.draw_text('Lives', [30, 50], TEXT_SIZE, 'White')
	canvas.draw_text(str(lives), [30, 70], TEXT_SIZE, 'White')
	
	canvas.draw_text('Score', [WIDTH-80, 50], TEXT_SIZE, 'White')
	canvas.draw_text(str(score), [WIDTH-80, 70], TEXT_SIZE, 'White')
	
	# draw ship and sprites
	my_ship.draw(canvas)	
	a_rock.draw(canvas)
	ship_missle.draw(canvas)

	# update ship and sprites
	my_ship.update()
	a_rock.update()
	ship_missle.update()
			
# timer handler that spawns a rock    
def rock_spawner():
	a_rock.rock_spawn()

# Random generator
def uniform(a, b):
    # Create random.uniform(a,b) function in simplegui
    return a + (b-a) * random.random()

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [0.3, 0.4], 0, 0.1, asteroid_image, asteroid_info)
ship_missle = Sprite([WIDTH / 2, HEIGHT / 2], [0,0], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

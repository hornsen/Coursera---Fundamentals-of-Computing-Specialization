# implementation of Spaceship - program template for RiceRocks

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
score = 0
lives = 3
time = 0
time_explosion = 0
started = False

rock_group = set([])
missile_group = set([])
explosion_group = set([])

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
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
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

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

	def __init__(self, pos, vel, angle, image, info):
		self.pos = [pos[0], pos[1]]
		self.vel = [vel[0], vel[1]]
		self.thrust = False
		self.angle = angle
		self.angle_vel = 0
		self.image = image
		self.image_center = info.get_center()
		self.image_size = info.get_size()
		self.radius = info.get_radius()

	def draw(self,canvas):
		if self.thrust:
			canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
		else:
			canvas.draw_image(self.image, self.image_center, self.image_size, 
			self.pos, self.image_size, self.angle)

	def update(self):
		# update angle
		self.angle += self.angle_vel

		# update position
		self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
		self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

		# update velocity
		if self.thrust:
			acc = angle_to_vector(self.angle)
			self.vel[0] += acc[0] * .1
			self.vel[1] += acc[1] * .1

		self.vel[0] *= .99
		self.vel[1] *= .99

	def set_thrust(self, on):
		self.thrust = on
		if on:
			ship_thrust_sound.rewind()
			ship_thrust_sound.play()
		else:
			ship_thrust_sound.pause()

	def increment_angle_vel(self):
		self.angle_vel += .05

	def decrement_angle_vel(self):
		self.angle_vel -= .05

	def shoot(self):
		global a_missile, missle_group
		forward = angle_to_vector(self.angle)
		missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
		missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
		a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
		
		missile_group.add(a_missile)
		
# Sprite class
class Sprite:
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
		
		self.lifespan = info.get_lifespan()
		
		if sound:
			sound.rewind()
			sound.play()
   
	def draw(self, canvas):
		global time_explosion

		if not self.animated:
			canvas.draw_image(self.image, self.image_center, self.image_size,
						  self.pos, self.image_size, self.angle)

		if self.animated == True:
			current_explosion_index = (time_explosion % self.lifespan) // 1
			current_explosion_center = [self.image_center[0] +  current_explosion_index * self.image_size[0], self.image_center[1]]
			canvas.draw_image(self.image, current_explosion_center, self.image_size, self.pos, self.image_size) 
			time_explosion += 1	

	def update(self):
		# update angle
		self.angle += self.angle_vel

		# update position
		self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
		self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
		
		# update age
		self.age += 1
		
		# Check if age is greater than lifespan
		if(self.age >= self.lifespan):
			return True

	def collide(self, other_object):
		if( dist(self.pos, other_object.pos) <= (other_object.radius + self.radius) ):
			return True

# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
	global started, lives, score
	center = [WIDTH / 2, HEIGHT / 2]
	size = splash_info.get_size()
	inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
	inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
	if (not started) and inwidth and inheight:
		reset()
		started = True	
			
		lives=3
		score=0

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

	# draw UI
	canvas.draw_text("Lives", [50, 50], 22, "White")
	canvas.draw_text("Score", [680, 50], 22, "White")
	canvas.draw_text(str(lives), [50, 80], 22, "White")
	canvas.draw_text(str(score), [680, 80], 22, "White")

	# draw ship and update ship
	my_ship.draw(canvas)
	my_ship.update()
		
	if started:
		# Process sprite groups
		process_sprite_group(rock_group, canvas)
		process_sprite_group(missile_group, canvas)
		process_sprite_group(explosion_group, canvas)
		
		# Check if missile hit asteroid
		group_group_collide(missile_group, rock_group)		
	
	else:
		# draw splash screen if not started
		canvas.draw_image(splash_image, splash_info.get_center(), 
			splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
			splash_info.get_size())

# timer handler that spawns a rock    
def rock_spawner():
	global rock_group
	rock_pos = [ WIDTH * random.random(), HEIGHT * random.random() ]
	rock_vel = [ 2*uniform( -random.random(), 2*random.random() ) , 2*uniform( -random.random(), 2*random.random() ) ]
	rock_avel = uniform(-0.1,0.1) 
	a_rock = Sprite(rock_pos, rock_vel, rock_avel, .1, asteroid_image, asteroid_info)
	
	if(len(rock_group) <= 12 and dist(rock_pos, my_ship.pos) > 4*my_ship.radius and started == True ): 
		rock_group.add( a_rock )   

# Process a sprite group (draw, updating, removing sprite)
def process_sprite_group(sprite_group, canvas):
	global lives, started
	
	for sprite in list(sprite_group):
		sprite.draw(canvas)
		sprite.update()
		
		if(sprite.update() == True):
			sprite_group.remove(sprite)
		
		if(sprite_group == rock_group and group_collide(sprite, my_ship) == True):
			sprite_group.remove(sprite)
			lives -= 1
			if(lives == 0):
				started=False		
				
# Check if there is a collision between a group and an object
def group_collide(sprite, other_object):
	if(sprite.collide(other_object) == True):
		explosion_group.add( Sprite(sprite.pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound) )
		return True		

# Check if there is a collision between two groups			
def group_group_collide(missile_group, rock_group):
	global score
	
	for missile in list(missile_group):
		for rock in list(rock_group):
			if(group_collide(missile, rock) == True):
				score += 10
				missile_group.discard(missile)
				rock_group.discard(rock)

# Reset the game
def reset():
	global rock_group, missile_group, explosion_group
	rewind_background_sound()
	play_background_sound()
	
	rock_group = set([])
	missile_group = set([])
	explosion_group = set([])

# Random generator
def uniform(a, b):
	return a + (b-a) * random.random()


# define callbacks
def play_background_sound():
	"""play some music, starts at last paused spot"""
	soundtrack.play()

def pause_background_sound():
	"""pause the music"""
	soundtrack.pause()

def rewind_background_sound():
	"""rewind the music to the beginning """
	soundtrack.rewind()

def vol_down():
	"""turn the current volume down"""
	global vol
	if vol > 0:
		vol = vol - 1
	soundtrack.set_volume(vol / 10.0)
	volume_button.set_text("Volume = " + str(vol))

def vol_up():
	"""turn the current volume up"""
	global vol
	if vol < 10:
		vol = vol + 1
	soundtrack.set_volume(vol / 10.0)
	volume_button.set_text("Volume = " + str(vol))


# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# set up control elements 
frame.add_label("Background sound")
frame.add_label("")
frame.add_button("play", play_background_sound,100)
frame.add_button("pause", pause_background_sound,100)
frame.add_button("rewind",rewind_background_sound,100)
frame.add_button("Vol down", vol_down,100)
frame.add_button("Vol up", vol_up,100)

# initialize volume, create button whose label will display the volume
vol = 7
volume_button = frame.add_label("Volume = " + str(vol))

# initialize ship 
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

import pygame

SOUNDS = {}
SND_VOLUME = 1.0
def play_sound(filename, volume=1.0):
	if filename not in SOUNDS:
		#SOUNDS[filename] = pygame.mixer.Sound(filepath(filename))
		SOUNDS[filename] = pygame.mixer.Sound(filename)
		SOUNDS[filename].set_volume(SND_VOLUME*volume)
	else:
		SOUNDS[filename].stop()
	SOUNDS[filename].play()
	return SOUNDS[filename]

def set_global_sound_volume(volume):
	global SND_VOLUME
	SND_VOLUME = volume


x_screen = 800
y_screen = 500
screensize = (x_screen,y_screen)
pygame.init()

clock = pygame.time.Clock()
pygame.mixer.init()


times = 0
over = False
while not over:
	clock.tick(30)
	if times % 1 == 0:
		play_sound("gunshot2.ogg",.4)
		print times
	times += 1
	if times > 200:
		over = True

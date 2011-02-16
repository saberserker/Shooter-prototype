import pygame
gvol = 1.0
snd = {}

def set_global_volume(volume):
	global gvol
	gvol = volume

def play_se(filenm, volume=1.0):
	if filenm not in snd:
		snd[filenm] = pygame.mixer.Sound(filenm)
		snd[filenm].set_volume(gvol*volume)
	else:
		snd[filenm].stop()
	snd[filenm].play()
	return snd[filenm]

def stop_se(filenm):
	if filenm in snd:
		snd[filenm].stop()


def play_music(filenm, loop=0, vol=1.0):
	pygame.mixer.music.load(filenm)
	pygame.mixer.music.set_volume(vol)
	pygame.mixer.music.play(loop)


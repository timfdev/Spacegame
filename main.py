''' 
Spacegame 9-11-2021 
Tim Frohlich
'''

import sys, pygame, time
from random import randrange

pygame.init()

# Global vars
WIDTH, HEIGHT = 750, 750
FONT = pygame.font.SysFont('ubuntumono', 40)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
N_ALIENS = 30

# Images
BACKGROUND = pygame.transform.scale(pygame.image.load('background-space.png'), (WIDTH, HEIGHT))
PLAYER_SHIP = pygame.transform.scale(pygame.image.load('red-spaceship.png'), (WIDTH/10, HEIGHT/10))
ALIEN_SHIP = pygame.transform.scale(pygame.image.load('alien_ship.png'), (WIDTH/10, HEIGHT/10))
LASER_BEAM = pygame.image.load('laser_red.png')
LASER_BEAM = pygame.transform.scale(LASER_BEAM, (LASER_BEAM.get_width()/2,LASER_BEAM.get_height()/2))


class Ship:
	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.img = img
		self.mask = pygame.mask.from_surface(self.img)
		self.lasers = []
		self.speed = randrange(40)

	def draw(self):
		WINDOW.blit(self.img, (self.x, self.y))
		for laser in self.lasers:
			laser.draw()

	def fire(self):
		laser = Laser(self.x, self.y)
		self.lasers.append(laser)

	def move(self):
		self.x += self.speed

	def move_lasers(self, score, aliens):
		for laser in self.lasers:
			laser.move()

			# Collision detection
			for alien in aliens:
				if laser.collision(alien):
					# Check if the laser is not already removed,
					# this happens when two ships get hit by the same laser.
					if laser in self.lasers:
						self.lasers.remove(laser)
					aliens.remove(alien)
					score += 1
			
			# Out of bounds detection 
			if laser.out_off_bounds():
				self.lasers.remove(laser)

		return score, aliens


class Laser:
	def __init__(self, x, y):
		self.x = x 
		self.y = y 
		self.img = LASER_BEAM
		self.mask = pygame.mask.from_surface(self.img)
		self.speed = 4

	def draw(self):
		WINDOW.blit(self.img, (self.x, self.y))

	def move(self):
		self.y -= self.speed
		self.speed *= 1.07

	def out_off_bounds(self):
		return self.y < -10

	def collision(self, obj):
		offset_x = obj.x - self.x
		offset_y = obj.y - self.y

		if self.mask.overlap(obj.mask, (offset_x, offset_y)) != None:
			return True


class Spacegame:
	def __init__(self): 
		self.running = True
		self.speed = 7
		self.score = 0
		self.aliens = [Ship(randrange(-WIDTH * 10, 0), randrange(HEIGHT/2), ALIEN_SHIP) for _ in range(N_ALIENS)]
		self.laser_cooldown = 0
		pygame.display.set_caption("Space game")

		# Menu game loop
		while self.running:
			WINDOW.blit(BACKGROUND, (0,0))
			menu_text = FONT.render('Press spacebar to begin', 1, (255,255,255))
			WINDOW.blit(menu_text, (WIDTH/2 - menu_text.get_width()/2,HEIGHT/2))
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.start_game()
		self.end_game()

	def start_game(self):
		player = Ship(WIDTH/2, HEIGHT - PLAYER_SHIP.get_height(), PLAYER_SHIP)
		clock = pygame.time.Clock()

		# Main game loop
		while self.running:
			# Setting Fps
			clock.tick(60)

			# Setting Background and text
			WINDOW.blit(BACKGROUND, (0,0))
			score_text = FONT.render('Score: ' + str(self.score), 1, (255,255,255))
			WINDOW.blit(score_text, (WIDTH - score_text.get_width() * 1.1, score_text.get_height()))
			
			# Draw and move aliens
			for alien in self.aliens:
				alien.draw()
				alien.move()
				if alien.x > WIDTH:
					self.aliens.remove(alien)

			#Draw and move player
			self.key_events(player)
			player.draw()

			# Move lasers and update score
			self.score, self.aliens = player.move_lasers(self.score, self.aliens)

			# End game cases
			if self.aliens == []:
				self.running = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit()

			# Updating the timer and display
			self.laser_cooldown += clock.get_time()		
			pygame.display.update()

	def key_events(self, player):
			keys = pygame.key.get_pressed()

			# Move left.
			if keys[pygame.K_LEFT] and player.x > 0:
				player.x -= self.speed

			# Move right.
			if keys[pygame.K_RIGHT] and player.x < WIDTH - PLAYER_SHIP.get_width():
				player.x += self.speed
				
			# The last fired laser must be more than 0.3s ago.
			if keys[pygame.K_SPACE] and self.laser_cooldown > 300:
				player.fire()
				self.laser_cooldown = 0	

	def end_game(self):
		WINDOW.fill((0,0,0,100))
		end_text = FONT.render('End score: ' + str(self.score) + ' out of ' + str(N_ALIENS) + ' killed', 1, (255,255,255))
		WINDOW.blit(end_text, (WIDTH/2 - end_text.get_width()/2,HEIGHT/2))
		pygame.display.update()
		time.sleep(3)
		pygame.quit()

if __name__ == "__main__":
	Spacegame()
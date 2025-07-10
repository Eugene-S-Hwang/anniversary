import pygame
import sys
import random
import asyncio

pygame.init()

# global variables
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
floor = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
pygame.display.set_caption('For Chaemin')

DARK_GREEN = (0, 150, 0)
SKY_BLUE = (105, 186, 255)
WHITE = (255,255,255)

#sprites
FALL_SPEED = 1
sprite_size = 20
heart_img = pygame.image.load(f"sprites/heart.png")
heart_img = pygame.transform.scale(heart_img, (sprite_size, sprite_size))
hearts = []
heart_score = 0

cat_img = pygame.image.load(f"sprites/cat.png")
cat_img = pygame.transform.scale(cat_img, (sprite_size * 2, sprite_size * 2))
cats = []
cat_score = 0

miffy_img = pygame.image.load(f"sprites/miffy.png")
miffy_img = pygame.transform.scale(miffy_img, (sprite_size * 2, sprite_size * 2))
miffys = []
miffy_score = 0

hach_img = pygame.image.load(f"sprites/hachiware.png")
hach_img = pygame.transform.scale(hach_img, (sprite_size * 2, sprite_size * 2))
hachs = []
hach_score = 0

pig_img = pygame.image.load(f"sprites/pig.png")
pig_img = pygame.transform.scale(pig_img, (sprite_size*3, sprite_size*3))
pig_rect = pygame.Rect(SCREEN_WIDTH/2, SCREEN_HEIGHT - 50 - sprite_size*2, sprite_size*3, sprite_size*3)

prom_font = pygame.font.Font(None, 60)

corny_y = 0
prom_y = 0
corny_text = prom_font.render("You've caught my heart", True, (255, 0, 0))
corny_text2 = prom_font.render("ever since I first met you.", True, (255, 0, 0))
prom_text = prom_font.render("Will you \"CODE\"", True, (255, 0, 0))
prom_text2 = prom_font.render("to PROM with me?", True, (255, 0, 0))

async def draw_setting():
	"""Draws background, platforms, floor, and banana onto our screen"""
	# For each new frame, we want to redraw our background over the previous frame
	pygame.draw.rect(screen, SKY_BLUE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

	# # Drawing the floor
	pygame.draw.rect(screen, DARK_GREEN, floor)


async def draw_scores():
	if(hach_score == 5):
		hach_txt = font.render(f"Hachiware Score: {hach_score}/5", True, (0,255,0))
	else:
		hach_txt = font.render(f"Hachiware Score: {hach_score}/5", True, (255,255,255))
	screen.blit(hach_txt, (10, 10))
	
	if(miffy_score == 16):
		miffy_txt = font.render(f"Miffy Score: {miffy_score}/16", True, (0,255,0))
	else:
		miffy_txt = font.render(f"Miffy Score: {miffy_score}/16", True, (255,255,255))
	screen.blit(miffy_txt, (10, 30))
	
	if(cat_score == 20):
		cat_txt = font.render(f"Cat Score: {cat_score}/20", True, (0,255,0))
	else:
		cat_txt = font.render(f"Cat Score: {cat_score}/20", True, (255,255,255))
	screen.blit(cat_txt, (10, 50))

	if(heart_score == 22):
		heart_txt = font.render(f"Heart Score: {heart_score}/22", True, (0,255,0))
	else:
		heart_txt = font.render(f"Heart Score: {heart_score}/22", True, (255,255,255))
	screen.blit(heart_txt, (10, 70))
	
	font.set_underline(True)
	obj = font.render("Objective: Catch all of the cute sprites!", True, (255, 255, 255))
	screen.blit(obj, (198, 10))
	font.set_underline(False)


async def spawn_heart():
    x = random.randint(0, SCREEN_WIDTH - sprite_size)
    heart = pygame.Rect(x, 0, sprite_size, sprite_size)
    hearts.append(heart)

async def spawn_cat():
	x = random.randint(0, SCREEN_WIDTH - sprite_size * 2)
	cat = pygame.Rect(x, 0, sprite_size * 2, sprite_size * 2)
	cats.append(cat)
	
async def spawn_miffy():
	x = random.randint(0, SCREEN_WIDTH - sprite_size * 2)
	miffy = pygame.Rect(x, 0, sprite_size * 2, sprite_size * 2)
	miffys.append(miffy)

async def spawn_hach():
	x = random.randint(0, SCREEN_WIDTH - sprite_size * 2)
	hach = pygame.Rect(x, 0, sprite_size * 2, sprite_size * 2)
	hachs.append(hach)

async def update_sprites():
	for heart in hearts:
		heart.y += FALL_SPEED
		print(FALL_SPEED)
	
	for cat in cats:
		cat.y += FALL_SPEED
	
	for miffy in miffys:
		miffy.y += FALL_SPEED
	
	for hach in hachs:
		hach.y += FALL_SPEED


async def update_text():
	global corny_y
	global prom_y

	if(corny_y > SCREEN_HEIGHT // 2):
		if(prom_y < SCREEN_HEIGHT // 2):
			prom_y += FALL_SPEED
		else:
			for _ in range(30):
				x = random.randint(0, SCREEN_WIDTH)
				y = random.randint(0, SCREEN_HEIGHT)
				screen.blit(heart_img, (x, y))
		
		screen.blit(prom_text, (188, prom_y))
		screen.blit(prom_text2, (165.5, prom_y + 50))
		if prom_y >= SCREEN_HEIGHT // 2:
			pygame.time.delay(2000)

	else:
		corny_y += FALL_SPEED
		screen.blit(corny_text, (118.5, corny_y))
		screen.blit(corny_text2, (103.5, corny_y + 50))
		if(corny_y > SCREEN_HEIGHT // 2):
			pygame.time.delay(2000)
		

async def collide_remove():
	global heart_score
	global cat_score
	global miffy_score
	global hach_score

	for heart in hearts[:]:
		if(heart.colliderect(floor)):
			hearts.remove(heart)
		elif heart.colliderect(pig_rect):
			hearts.remove(heart)
			if(heart_score < 22):
				heart_score += 1

	for cat in cats[:]:
		if(cat.colliderect(floor)):
			cats.remove(cat)
		elif cat.colliderect(pig_rect):
			cats.remove(cat)
			if cat_score < 20:
				cat_score += 1
	
	for miffy in miffys[:]:
		if(miffy.colliderect(floor)):
			miffys.remove(miffy)
		elif miffy.colliderect(pig_rect):
			miffys.remove(miffy)
			if miffy_score < 16:
				miffy_score += 1
		
	for hach in hachs[:]:
		if(hach.colliderect(floor)):
			hachs.remove(hach)
		elif hach.colliderect(pig_rect):
			hachs.remove(hach)
			if hach_score < 5:
				hach_score += 1



async def main():
	global frame

	running = True
	# spawn_timer = 0
	# spawn_int = 60
	prev = 0
	
	while running == True:
		
		# Here is an instance of event handling, checking if the user wants to exit
		pygame.time.delay(10)
		dt = pygame.time.get_ticks()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				sys.exit()
		
		await draw_setting()
		await draw_scores()
		
		key_pressed = pygame.key.get_pressed()
		if key_pressed[pygame.K_a] and pig_rect.x >= 3:
			pig_rect.x -= 3
		elif key_pressed[pygame.K_d] and pig_rect.x <= SCREEN_WIDTH - sprite_size*3:
			pig_rect.x += 3
		screen.blit(pig_img, pig_rect)
        
		if dt - prev > 1000:
			choose = random.randint(1, 63)
			if(41 < choose):
				await spawn_heart()
			
			elif 21 < choose < 42:
				await spawn_cat()
			
			elif 5 < choose < 22:
				await spawn_miffy()
			
			else:
				await spawn_hach()

			prev = dt
		
		await update_sprites()
		
		await collide_remove()
		
		for heart in hearts:
			screen.blit(heart_img, heart)
			
		for cat in cats:
			screen.blit(cat_img, cat)
		
		for miffy in miffys:
			screen.blit(miffy_img, miffy)
		
		for hach in hachs:
			screen.blit(hach_img, hach)

		# Rest of game loop goes here
		if hach_score == 5 and miffy_score == 16 and cat_score == 20 and heart_score == 22:
			await draw_setting()
			await update_text()
		
		pygame.display.update()
		await asyncio.sleep(0)
		
asyncio.run(main())
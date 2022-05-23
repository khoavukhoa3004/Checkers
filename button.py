from matplotlib.backend_bases import LocationEvent
import pygame,sys
'''
button của pygame
'''
class Button:
	'''
	Create button for UI design
	'''
	def __init__(self, locaton: list, width, height, text):

		self.width = width
		height = height
		self.locaton = locaton
		self.rect =  pygame.Rect( locaton, (width, height))
		self.rect.topleft = self.locaton
		self.buttonColor = (255,255,255)
		self.clicked = False
		font1 = pygame.font.Font(None,30)
		self.fontButton = font1.render(text, True, (0,0,0))
		self.action = False
	def draw(self, surface):
		self.action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				self.action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		if self.action == True:
			self.buttonColor = (152,251,152)
			pygame.draw.rect(surface, self.buttonColor,self.rect)
		else: 
			self.buttonColor = (255,255,255)
			pygame.draw.rect(surface, self.buttonColor,self.rect)
		
		
		surface.blit(self.fontButton, (self.locaton[0] + 15, self.locaton[1] + 15))


		return self.action

import pygame
import time
from time import strftime
from itertools import islice
import random
import math

from constantes import *


gameDisplay = pygame.display.set_mode((display_width,display_height))

class blocos:
    def __init__(self, color=black, x=100, y=100):
        self.color=color
        self.x=x
        self.y=y
        self.width=50
        self.height=15
        self.font=pygame.font.SysFont(None, 25)

    def draw_block(self):
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.width, self.height])
    
class jogador:
    def __init__(self):
        self.vel = 0
        self.width=80
        self.height=20
        self.color=black
        self.pos = [display_width*0.45, display_height-2*self.height]

    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, [self.pos[0], self.pos[1], self.width, self.height])
        
        #font = pygame.font.SysFont(None, 25)
       # text = font.render("Vel_x: " + str(self.vel), True, black)
        #gameDisplay.blit(text, (0, 10))

class bola:
	def __init__(self, pos, color=white, vel=[0, 4]):
		self.color=color
		self.pos=pos
		self.raio=10
		self.vel=vel

	def draw(self):
		pygame.draw.circle(gameDisplay, self.color, self.pos, self.raio)

	def reset(self, pos, vel):
		self.pos = pos
		self.vel = vel 

class msg:
    def __init__(self, text, font, tamanho, pos=(display_width/2, display_height/2), color=black):
        self.text = text
        self.font=font
        self.tamanho=tamanho
        self.pos=pos
        self.color=color
        
    def text_objects(self, lt):
        textSurface=lt.render(self.text, True, self.color)
        return textSurface, textSurface.get_rect()
    
    def message_display(self):
        largeText = pygame.font.Font(self.font, self.tamanho)
        TextSurf, TextRect = self.text_objects(largeText)
        TextRect.center = self.pos
        gameDisplay.blit(TextSurf, TextRect)

    def crash(self):
        largeText = pygame.font.Font(self.font, self.tamanho)
        TextSurf, TextRect = self.text_objects(largeText)
        TextRect.center = self.pos
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        time.sleep(1)

class button:
	def __init__(self, msg, coord, cori, cora, acao=None):
		self.msg=msg
		self.coord=coord
		self.cori=cori
		self.cora=cora
		self.acao=acao
	def draw(self):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		if self.coord[0] + self.coord[2] > mouse[0] > self.coord[0] and self.coord[1] + self.coord[3] > mouse[1] > self.coord[1]:
			pygame.draw.rect(gameDisplay, self.cora, self.coord)
			if click[0]==1 and self.acao != None:
				self.acao()
		else:
			pygame.draw.rect(gameDisplay, self.cori, self.coord)
		men = msg(self.msg, "freesansbold.ttf", 20, (self.coord[0] + self.coord[2]/2, self.coord[1] + self.coord[3]/2), black)
		men.message_display()

def quitgame():
	pygame.quit()
	quit()


class c_recordes:
    def __init__(self, lst_controle, rec):
        self.lst_controle=lst_controle
        self.rec=rec
        if lst_controle==[1,0,0,0]:
            self.string = "recordes_mouse.txt"
        elif lst_controle==[0,1,0,0]:
        	self.string = "recordes_teclado.txt"
        elif lst_controle==[0,0,1,0]:
        	self.string = "recordes_ds4.txt"
        elif self.lst_controle==[0,0,0,1]:
        	self.string = "recordes_cam.txt"

    def app_recorde(self):
        try:
            self.data = strftime("%a, %d %b %Y %H:%M:%S    ", time.localtime())
            self.line = "Recorde: {:3}".format(self.rec) + "      " + self.data+ "\n"
            with open(self.string, "at") as f:
                f.write(self.line)
        except:
            print("Erro ao gravar o recorde!\n")

    def read_recorde(self):
        try:
            self.recs = []
            with open(self.string, "rt") as f:
                for self.lin in islice(f, 30):
                    self.aux=int(self.lin[9:14])
                    self.data = self.lin[18:43]
                    self.recs.append((self.aux, self.data))
            return (self.recs)
        except:
            print("Erro ao ler o recorde!\n")

#INTERNET TEMPORÁRIO
def collision(rleft, rtop, width, height,   
              center_x, center_y, radius):  
    
    rright, rbottom = rleft + width, rtop + height

    cleft, ctop     = center_x-radius, center_y-radius
    cright, cbottom = center_x+radius, center_y+radius


    if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        return False  

    for x in (rleft, rleft+width):
        for y in (rtop, rtop+height):
            if math.hypot(x-center_x, y-center_y) <= radius:
                return True
    if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        return True 
    return False
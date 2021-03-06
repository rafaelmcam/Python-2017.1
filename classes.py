import pygame
import time
from time import strftime
from itertools import islice
import random
import math

from constantes import *


gameDisplay = pygame.display.set_mode((display_width,display_height))


class special_comb:
    def __init__(self,x=0,y=0,ativar=False):
        self.x=x
        self.y=y
        self.ativar=ativar
    def draw(self,vel,imagem):
        self.y+=vel
        self.imagem=imagem
        gameDisplay.blit(self.imagem,(self.x,self.y))
        #pygame.draw.circle(gameDisplay, (0,0,0), (self.x,self.y), self.raio)

class life:
    def __init__(self,imagem,num_lifes):
        self.imagem = imagem
        self.l_width=5
        self.l_height=5
        self.num_lifes = num_lifes

    def draw(self,actual):
        self.l_width=5
        self.l_height=5
        self.num_lifes=actual
        if self.num_lifes>=0:
            for _ in range(0,self.num_lifes):
                gameDisplay.blit(self.imagem,(self.l_width,5))
                self.l_width+=39
        else:
            for _ in range(0,-self.num_lifes):
                self.l_width-=39
                gameDisplay.blit(self.imagem,(self.l_width,5))

class blocos:
    def __init__(self, x=100, y=100, vida = 1, identity = 0, invencible = False):
        self.vida = vida
        self.color=self.define_color()
        self.x=x
        self.y=y
        self.width=50
        self.height=15
        self.identity=identity
        self.invencible=invencible
        self.font=pygame.font.SysFont(None, 25)

    def eqs(self, x):
        return (self.y + (self.height/self.width)*(x-self.x)), (self.y+self.height - (self.height/self.width)*(x-self.x))
        
    def tupla_bol(self, x, y):
        tupla = (self.eqs(x)[0]>y,self.eqs(x)[1]>y)
        return tupla
        if tupla == (True, True):
            return "Cima"
        elif tupla == (False, False):
            return "Baixo"
        elif tupla == (True, False):
            return "Direita"
        elif tupla == (False, True):
            return "Esquerda"

    def draw_block(self):
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.width, self.height])

    def define_color(self):
        d = {0:None, 1: black, 2:green, 3:blue, 4:white}
        return d[self.vida]
    
class jogador:
    def __init__(self,width=80):
        self.velmouse = 0
        self.velteclado = 0
        self.velds4 = 0
        self.velcam = 0
        self.width=width
        self.height=20
        self.color=black
        self.pos = [display_width*0.45, display_height-2*self.height]
        self.x = self.pos[0]
        self.y = self.pos[1]

    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, [self.pos[0], self.pos[1], self.width, self.height])

    def eqs(self, x):
        return (self.y + (self.height/self.width)*(x-self.x)), (self.y+self.height - (self.height/self.width)*(x-self.x))
        
    def tupla_bol(self, x, y):
        tupla = (self.eqs(x)[0]>y,self.eqs(x)[1]>y)
        return tupla
        if tupla == (True, True):
            return "Cima"
        elif tupla == (False, False):
            return "Baixo"
        elif tupla == (True, False):
            return "Direita"
        elif tupla == (False, True):
            return "Esquerda"
        
        #font = pygame.font.SysFont(None, 25)
       # text = font.render("Vel_x: " + str(self.vel), True, black)
        #gameDisplay.blit(text, (0, 10))

class bola:
	def __init__(self, pos, color=white, vel=vel_inicial_bola.copy()):
		self.color=color
		self.pos=pos
		self.posanterior = []
		self.raio = raio_bola
		self.vel=vel

	def draw(self,color):
		pygame.draw.circle(gameDisplay, color, self.pos, self.raio)

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
                for self.lin in islice(f, 300):
                    self.aux=int(self.lin[9:14])
                    self.data = self.lin[18:43]
                    self.recs.append((self.aux, self.data))
            return (self.recs)
        except:
            print("Erro ao ler o recorde!\n")


def coli (recx, recy, recwidth, recheight, ballx, bally, ballraio):
	Dx =  ballx - max(recx, min(ballx, recx+recwidth))
	Dy =  bally - max(recy, min(bally, recy+recheight))
	return (Dx*Dx+Dy*Dy < ballraio*ballraio)


#pygame.image.load retorna uma surface, usa-se pygame.surfarray.pixels3d para transformar em um array parecido com o scipy-image
def color_surface(surface, red, green, blue):
    arr = pygame.surfarray.pixels3d(surface)
    arr[:,:,0] += red
    arr[:,:,1] += green
    arr[:,:,2] += blue

import pygame
import time
import random
import numpy as np
import cv2

from constantes import *
from classes import *

pygame.init()

pygame.display.set_caption('Projeto Python 2017.1')
clock = pygame.time.Clock()

controle = [1, 0, 0, 0]
seletor = [1, 0, 0, 0]

def game_intro():
	b_jogar = button("Jogar", botao_jogar, green, bright_green, game_loop)
	b_sair = button("Sair", botao_sair, red, bright_red, quitgame)
	b_recordes = button("Recordes", botao_recordes, blue, bright_blue, recordes)
	b_controles = button("Controles", botao_controles, yellow, bright_yellow, controles)
	men = msg("Projeto Python 2017.1", "freesansbold.ttf", 50, (display_width/2, display_height/6), gray)
	men2 = msg("Diógenes Wallis", "freesansbold.ttf", 20, (display_width/3, display_height/2 - 90), gray)
	men3 = msg("Rafael Campello", "freesansbold.ttf", 20, (display_width/3, display_height/2 - 40), gray)
	men5 = msg("Professor: Hermano Cabral", "freesansbold.ttf", 20, (display_width/3 + 53, display_height/2+10), gray)
	men4 = msg("Selecione um controle", "freesansbold.ttf", 20, (botao_controles[0]+60, botao_controles[1]-30), green)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.fill(black)
		
		men.message_display()
		men2.message_display()
		men3.message_display()
		men5.message_display()
		if controle==[0,0,0,0]:
			men4.message_display()
		if controle==[1,0,0,0] or controle==[0,1,0,0] or controle==[0,0,1,0] or controle==[0,0,0,1]:
			b_jogar.draw()
		b_sair.draw()
		b_recordes.draw()
		b_controles.draw()
		pygame.display.update()

		clock.tick(15)

def recordes():
	b_voltar = button("Voltar", botao_voltar, blue, bright_blue, game_intro)
	b_s1 = button("Mouse", botao_mouse2, dark_gray, gray, s_1)
	b_s2 = button("Teclado", botao_teclado2, dark_gray, gray, s_2)
	b_s3 = button("DS4", botao_ds42, dark_gray, gray, s_3)
	b_s4 = button("Câmera", botao_camera2, dark_gray, gray, s_4)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		rec = c_recordes(seletor, 0)
		recs = sorted(rec.read_recorde())[::-1]
		lst_men = []

		for i, x in enumerate(recs[:8]):
			lst_men.append(msg("{} -- {}".format(x[0], x[1]), "freesansbold.ttf", 20, (display_width/2, 300+i*30), gray))

		gameDisplay.fill(black)
		for x in lst_men:
			x.message_display()

		men = msg("Selecionado: {}".format(seletor), "freesansbold.ttf", 20, (display_width/2, 100), gray)
		men.message_display()

		b_voltar.draw()
		b_s1.draw()
		b_s2.draw()
		b_s3.draw()
		b_s4.draw()
		pygame.display.update()
		clock.tick(15)

def c_mouse():
	global controle
	controle = [1, 0, 0, 0]
def c_teclado():
	global controle
	controle = [0, 1, 0, 0]
def c_ds4():
	global controle
	controle = [0, 0, 1, 0]
def c_cam():
	global controle
	controle = [0, 0, 0, 1]

def s_1():
	global seletor
	seletor = [1, 0, 0, 0]
def s_2():
	global seletor
	seletor = [0, 1, 0, 0]
def s_3():
	global seletor
	seletor = [0, 0, 1, 0]
def s_4():
	global seletor
	seletor = [0, 0, 0, 1]

def controles():
	global controle
	b_voltar = button("Voltar", botao_voltar, yellow, bright_yellow, game_intro)
	b_mouse = button("Mouse", botao_mouse, gray, white, c_mouse)
	b_teclado = button("Teclado", botao_teclado, gray, white, c_teclado)
	b_ds4 = button("DS4", botao_ds4, gray, white, c_ds4)
	b_cam = button("Câmera", botao_camera, gray, white, c_cam)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		string = "Selecionado: " + str(controle)
		men = msg(string, "freesansbold.ttf", 20, (display_width/2, 550), white)
		gameDisplay.fill(black)
		b_voltar.draw()
		b_mouse.draw()
		b_teclado.draw()
		b_ds4.draw()
		b_cam.draw()
		men.message_display()

		pygame.display.update()
		clock.tick(15)

def game_loop():
	font=pygame.font.SysFont(None, 25)
	global phat
	score=0
	lst_col = time.time()

	if controle == [0, 0, 0, 1]:
		cap = cv2.VideoCapture(0)

	if controle == [0, 0, 1, 0]:
		try:
			pygame.joystick.init()
			joystick = pygame.joystick.Joystick(0)
			joystick.init()
			print(joystick.get_name())
		except:
			print("DS4 não conectado!")
			time.sleep(3)
			game_intro()

	player = jogador()
	ball = bola(pos_inicial_bola, black)


	block_list = []
	for i in range(qblocosx):
		for j in range(qblocosy):
			block_list.append(blocos(60+i*70, 60+j*60, 4))

	mencrash = msg("Você Perdeu!", "freesansbold.ttf", 100)

	last = [0, 0]

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if controle == [0, 1, 0, 0]:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						player.vel = -5
					if event.key == pygame.K_RIGHT:
						player.vel = 5
					if event.key == pygame.K_UP:
						player.vel = -5
					if event.key == pygame.K_DOWN:
						player.vel = 5

				if event.type == pygame.KEYUP:
					if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
						player.vel = 0
					if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
						player.vel = 0

		if controle == [0, 0, 1, 0]:
			hat = joystick.get_hat(0)
			if hat[0]==1 and phat[0]!=1:
				player.vel = 5
			if hat[0]==-1 and phat[0]!=-1:
				player.vel = -5
			if hat[0]==0:
				player.vel = 0
			phat=hat

		if controle == [1, 0, 0, 0]:
			mouse_tuple=pygame.mouse.get_pos()
			player.pos[0] = mouse_tuple[0] - player.width/2

		if controle == [0, 0, 0, 1]:
			_, frame = cap.read()
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			lower_blue = np.array([90, 100, 100])
			upper_blue = np.array([130, 255, 255])
			mask = cv2.inRange(hsv, lower_blue, upper_blue)

			element = cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))
			mask = cv2.erode(mask,element, iterations=2)
			#mask = cv2.dilate(mask,element,iterations=2)
			#mask = cv2.erode(mask,element)

			frame, contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

			maxArea = 0
			melhorContorno = None


			for contorno in contornos:
				cArea = cv2.contourArea(contorno)
				if cArea > maxArea:
					melhorContorno = contorno
					maxArea = cArea

			if melhorContorno is not None and cArea>2000:
				x,y,w,h = cv2.boundingRect(melhorContorno)
				cv2.rectangle(frame, (x,y),(x+w,y+h), (255,255, 255), 5)
				player.pos[0] = int((1270-x-(w/2))*(800/1270))


		player.pos[0] += player.vel
		ball.pos[0] += ball.vel[0]
		ball.pos[1] += ball.vel[1]


		gameDisplay.fill(red)


		men = msg("Score: {}".format(score), "freesansbold.ttf", 20, (40, 20), black)
		men.message_display()

		score = qblocosx*qblocosy-len(block_list)

		if ball.pos[0] > display_width - ball.raio:
			ball.vel[0] = -abs(ball.vel[0])
			last = [0, 0]
		elif ball.pos[0] < ball.raio:
			ball.vel[0] = abs(ball.vel[0])
			last = [0, 0]
		elif ball.pos[1] < ball.raio:
			ball.vel[1] =  abs(ball.vel[1])
			last = [0, 0]
		elif ball.pos[1] + ball.raio > display_height:
			rec = c_recordes(controle, score)
			rec.app_recorde()

			mencrash.crash()


			ball.reset([int(player.pos[0]+100), int(player.pos[1]-player.height-200)], [0, 4])
			block_list = []
			for i in range(qblocosx):
				for j in range(qblocosy):
					block_list.append(blocos(60+i*70, 60+j*40, 4))

		if coli(player.pos[0], player.pos[1], player.width, player.height, ball.pos[0], ball.pos[1], ball.raio):
			ball.vel[1] = -abs(ball.vel[1])
			ball.vel[0] += int((ball.pos[0]-(player.pos[0] + player.width/2))/30)
			last = [0, 0]
			'''MUDANÇA DA VEL X DEPENDER DA VELOCIDADE DO PLAYER E NÃO DA POSIÇÃO QUE TOCA NO PLAYER'''
		for bloco in block_list:
			if coli(bloco.x, bloco.y, bloco.width, bloco.height, ball.pos[0], ball.pos[1], ball.raio) and last!=[bloco.x, bloco.y]:
				if bloco.tupla_bol(ball.pos[0], ball.pos[1]) == (False, False):
					ball.vel[1] = abs(ball.vel[1])
					bloco.vida -= 1
					print("colidiu em baixo")
				elif bloco.tupla_bol(ball.pos[0], ball.pos[1]) == (True, True):
					ball.vel[1] = -abs(ball.vel[1])
					bloco.vida -= 1
					print("colidiu em cima")
				elif bloco.tupla_bol(ball.pos[0], ball.pos[1]) == (True, False):
					ball.vel[0] = abs(ball.vel[0])
					bloco.vida -= 1
					print("colidiu do lado direito")
				elif bloco.tupla_bol(ball.pos[0], ball.pos[1]) == (False, True):
					ball.vel[0] = -abs(ball.vel[0])
					bloco.vida -= 1
					print("colidiu do lado esquerdo")
				'''FAZER CONDIÇÕES IF PARA VER DE ONDA A BOLA ESTÁ VINDO E USAR ABS DIFERENTE PARA CADA UM'''
				'''FAZER DETECÇÃO DE COLISÃO HORIZONTAL E MUDAR TAMBEM A VELOCIDADE X!!!'''
				bloco.color=bloco.define_color()
				if bloco.vida == 0:
					block_list.remove(bloco)
				
				print("Anterior: {}, Bloco Atual: {}".format(last, [bloco.x, bloco.y]))
				last = [bloco.x, bloco.y]
				#time.sleep(0.1)


		if player.pos[0] > display_width-player.width:
			player.pos[0] = display_width-player.width
		elif player.pos[0] < 0:
			player.pos[0] = 0


		for i in block_list:
			i.draw_block()

		player.draw()
		ball.draw()

		pygame.display.update()
		clock.tick(60*3)

game_intro()
pygame.quit()
quit()

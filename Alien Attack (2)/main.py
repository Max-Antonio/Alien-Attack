from ast import Return
from pickle import FALSE
import pygame
import random
from pygame import mixer

pygame.init() # inicializa o pygame

# musica de fundo

mixer.music.load("Carosone_-_Peace_and_Agitation.wav")
toca_musica = -1
mixer.music.play(toca_musica)
mixer.music.set_volume(0.2) #vai de 0.0 a 1.0

# funções

def jogador(x, y):
    tela.blit(jogador_img , (x, y))

def inimigo(x, y, i):
    tela.blit(inimigo_img[i] , (x, y))

def bala_atira(x, y):
    global bala_estado
    bala_estado = "atira"
    tela.blit(bala_img, (x + 16, y + 10))

def colide(inimigox, inimigoy, balax, balay):
    distancia = ((inimigox - balax)**2 + (inimigoy - balay)**2)**0.5
    if distancia < 27 and bala_estado == "atira":
        return True
    else:
        return False

def mostra_score(x,y):
    score = font.render("Pontos: " + str(score_value), True, (255,255,255))
    tela.blit(score , (x, y))

def game_over_texto():
    game_over = over_font.render("FIM DE JOGO", True, (255,255,255))
    game_over2 = font.render("Pontuação: " + str(score_value), True, (100,100,200))
    game_over_r = font.render("Aperte R para recomeçar", True, (255,255,255))
    tela.blit(game_over , (200, 250))
    tela.blit(game_over2 , (300, 340))
    tela.blit(game_over_r , (210, 440))

def mostra_tutorial():
    tutorial = font.render("Aperte X para atirar e <- -> para se mover ", True, (255,255,255))
    tela.blit(tutorial, (80, 250))

def restart():
    global score_value, vel_jogador, move_balay, pode_mover, lista_lugares, indo_direita, indo_esquerda
    score_value = 0
    for i in range(n_inimigos):
        if i == 1:
            inimigox[i] = 1
            lista_lugares.append(1)
        else:
            x = escolhe_inimigox(lista_lugares)
            inimigox[i] = x
            lista_lugares.append(x)
        inimigoy[i] = random.choice([50,120,190])
        move_inimigox[i] = 0.5
        inimigo_img[i] = pygame.image.load("alien_invader.png")
    vel_jogador = 0.8
    move_balay = 2.1
    pode_mover = True
    indo_esquerda = False
    indo_direita = False

def escolhe_inimigox(ocupados):
    lugares = [1, 70, 139, 208, 277, 346, 415, 484, 553, 622, 691]
    for elem in lugares:
        if elem in ocupados:
            lugares.remove(elem)
    if lugares == []:
        return random.choice([1, 70, 139, 208, 277, 346, 415, 484, 553, 622, 691])
    else:
        x = random.choice(lugares)
        return x

def novo_lugar(posx, posy):
    if posx >= 736:
        posx = 1
        posy = posy + 70
    for i in range(n_inimigos):
        if inimigox[i] < posx + 69 and inimigox[i] > posx - 69 and posy == inimigoy[i]:
            return novo_lugar(posx + 138, posy)
    return posx, posy


# tela

tela = pygame.display.set_mode((800,600)) # cria a tela

# imagem de fundo

fundo = pygame.image.load("universe.png")

tutorial = True

# título e ícone
pygame.display.set_caption("Alien Attack")

icon = pygame.image.load("nave.png")
pygame.display.set_icon(icon)

# score
score_value = 0
font = pygame.font.Font('FreeSansBold.ttf', 32)

textox = 10
textoy = 10

# game over texto
over_font = pygame.font.Font('FreeSansBold.ttf', 64)

# jogador
jogador_img = pygame.image.load("nave.png")
jogadorx = 370
jogadory = 480
move_jogx = 0
move_jogy = 0

vel_jogador = 1

pode_mover = True
# inimigo
inimigo_img = []
inimigox = []
inimigoy = []
move_inimigox = []
move_inimigoy = []
n_inimigos = 10

lista_lugares = []

for i in range(n_inimigos):
    inimigo_img.append(pygame.image.load("alien_invader.png"))
    if i == 1:
        inimigox.append(1)
        lista_lugares.append(1)
    else:
        x = escolhe_inimigox(lista_lugares)
        inimigox.append(x)
        lista_lugares.append(x)
    inimigoy.append(random.choice([50,120,190]))
    move_inimigox.append(0.5)
    move_inimigoy.append(70)

# bala
'''
pronta: a bala não aparece
atira: a bala está se movendo
'''

bala_img = pygame.image.load("bala.png")
balax = 0
balay = 480
move_balax = 0
move_balay = 2.5
bala_estado = "pronta"


indo_direita = False
indo_esquerda = False 

running = True
while running:
    # fundo
    tela.blit(fundo,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # inputs de movimento
        if event.type == pygame.KEYDOWN:
            tutorial = False
            if event.key == pygame.K_r:
                restart()
            if event.key == pygame.K_LEFT and pode_mover:
                move_jogx = -vel_jogador
                indo_esquerda = True
            if event.key == pygame.K_RIGHT and pode_mover:
                move_jogx = vel_jogador
                indo_direita = True
            if event.key == pygame.K_x and pode_mover: # tecla x para atirar
                if bala_estado == "pronta":
                    bala_som = mixer.Sound("laser.wav")
                    bala_som.play()
                    balax = jogadorx
                    bala_atira(balax, balay)
        # restart

        if event.type == pygame.KEYUP and pode_mover:
            if event.key == pygame.K_LEFT and indo_direita == True:
                move_jogx = vel_jogador
                indo_esquerda = False
            elif event.key == pygame.K_RIGHT and indo_esquerda == True:
                move_jogx = -vel_jogador
                indo_direita = False
            elif event.key == pygame.K_LEFT:
                move_jogx = 0
                indo_esquerda = False
            elif event.key == pygame.K_RIGHT:
                move_jogx = 0
                indo_direita = False
        

    # movimento jogador
    jogadorx += move_jogx
    # barreiras
    if jogadorx >= 800:
        jogadorx = 0
    elif jogadorx <= -64:
        jogadorx = 736
    # movimento inimigo
    for i in range(n_inimigos):
        # game over
        if inimigoy[i] > 440:
            for j in range(n_inimigos):
                inimigoy[j] = 2000
            move_jogx = 0
            pode_mover = False
            tutorial = False
            game_over_texto()
            break

        inimigox[i] += move_inimigox[i]

        if inimigox[i] >= 736 or inimigox[i] <= 0:
            move_inimigox[i] = (-1)*move_inimigox[i]
            inimigoy[i] += move_inimigoy[i]
        # colisão
        colisao = colide(inimigox[i], inimigoy[i], balax, balay)
        if colisao:
            colide_som = mixer.Sound("explosao.wav")
            colide_som.play()
            balay = 480
            bala_estado = "pronta"
            score_value += 1
            if inimigox[i] in lista_lugares:
                lista_lugares.remove(inimigox[i])
            novo_lugarx, novo_lugary = novo_lugar(escolhe_inimigox(lista_lugares), 50)
            inimigox[i] = novo_lugarx
            inimigoy[i] = novo_lugary
            lista_lugares.append(novo_lugar)
            # progressão de dificuldade
            if score_value == 50:
                for k in range(n_inimigos):
                    inimigo_img[k] = pygame.image.load("alien_invader (2).png")
                    move_inimigox[k] = move_inimigox[k]*1.15
            elif score_value == 100:
                for k in range(n_inimigos):
                    inimigo_img[k] = pygame.image.load("alien_invader (3).png")
                    move_inimigox[k] = move_inimigox[k]*1.20
            elif score_value == 200:
                for k in range(n_inimigos):
                    inimigo_img[k] = pygame.image.load("alien_invader (4).png")
                    move_inimigox[k] = move_inimigox[k]*1.30
            elif score_value % 10 == 0 and score_value > 0:
                for k in range(n_inimigos):
                    move_inimigox[k] = move_inimigox[k]*1.02
                vel_jogador = vel_jogador + 0.1
                move_balay = move_balay*1.03
        inimigo(inimigox[i], inimigoy[i], i)

    # movimento bala
    if balay < -10:
        balay = 480
        bala_estado = "pronta"
    if bala_estado == "atira":
        bala_atira(balax, balay)
        balay -= move_balay

    if tutorial:
        mostra_tutorial()
    mostra_score(textox, textoy)
    jogador(jogadorx, jogadory)
    pygame.display.update()

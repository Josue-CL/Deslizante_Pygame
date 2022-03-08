from cgitb import text
from imp import reload
from operator import ne
import random
from typing import List, Text

import pygame
pygame.mixer.init()
import time
#definicion de colores
blanco = (255,255,255)
negro = (0,0,0)
rojo = (255,0,0)

#definicion del tamaño de la pantalla
display_ancho = 800
display_alto = 600

pygame.init()
superficie = pygame.display.set_mode((display_ancho,display_alto))
pygame.display.set_caption('deslizante')    #Implementamos el titulo

#definimos fondo del juego
fondo_snake = pygame.image.load("fondoJuego.jpg").convert()
imagen_redimensionada3 = pygame.transform.scale(fondo_snake,(display_ancho,display_alto))
#defenimos el fondo del intro y pausa
fondo_game = pygame.image.load("snake.webp").convert()
imagen_redimensionada = pygame.transform.scale(fondo_game,(display_ancho,display_alto))
reloj = pygame.time.Clock()

#definimos el fondo del game over
fondo_gameover = pygame.image.load("perdiste.jpg").convert()
imagen_redimensionada2 = pygame.transform.scale(fondo_gameover,(display_ancho,display_alto))

#definimos variables
bloque_tamano =20
FPS = 25   #Velocidad de la vibora

#Musica
sonido_fondo = pygame.mixer.Sound("Musica_pingpong.mpeg")
pygame.mixer.Sound.play(sonido_fondo, -1) # Con -1 indicamos que queremos que se repita indefinidamente

#fuentes
Smallfont = pygame.font.SysFont("comicsansms", 25)
MedFond = pygame.font.SysFont("comicsansms", 50)
BigFond = pygame.font.SysFont("comicsansms", 80)

def pausa():
    pausado = True
    while pausado: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_c:
                    pausado = False
                elif event.key ==pygame.K_q:
                    pygame.quit()
                    quit()

        superficie.blit(imagen_redimensionada, [0,0])
        message_to_screen("Pausado", negro,-100, "mediano")
        message_to_screen("Presiona C para continuar y Q para terminar", negro,25, "pequeno")
        pygame.display.update()
        reloj.tick(5)

def puntos(score):
    text = Smallfont.render("Puntos: " + str(score), True, negro) 
    superficie.blit(text, [0,0])

def intro_juego():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()    
                
        superficie.blit(imagen_redimensionada, [0,0])
        message_to_screen("Bienvenidos a deslizante",rojo,-100, "mediano")
        message_to_screen("El objetivo del juego es comer la manzana roja",negro,-50, "pequeno")
        message_to_screen("Mientas mas manzanas comas, Mas grande se pone la serpiente",negro,-30, "pequeno")
        message_to_screen("Si chocas con la pared y si te comes a ti mismo mueres",negro,-10, "pequeno")
        message_to_screen("Precione C para Jugar y Q para terminar",negro,180, "pequeno")
        pygame.display.update()
        reloj.tick(FPS)

def serpiente(bloque_tamano, listaSerp):
    for XiY in listaSerp:
        pygame.draw.rect(superficie, negro, [XiY[0], XiY[1],bloque_tamano,bloque_tamano])

#Se define el tamano de los mensajes
def text_objetos(text,color, TamLet):
    if TamLet == "pequeno":
        TextSup = Smallfont.render(text, True, color)
    elif TamLet == "mediano":
        TextSup = MedFond.render(text, True, color)
    elif TamLet == "grande":
        TextSup = BigFond.render(text, True, color)
    return TextSup, TextSup.get_rect()

#mostramos un texto
def message_to_screen(msg, color, y_displace =0, TamLet = "pequeno"):
    textSur, textRect = text_objetos(msg, color, TamLet)
    textRect.center = (display_ancho/2), (display_alto/2) + y_displace
    superficie.blit(textSur, textRect)
#pantalla_texto = font.render(msg, True, color)
#superficie.blit(pantalla_texto, [display_ancho/2, display_alto/2])



def gameLoop():
    gameExit = False
    gameOver = False

    lead_x = display_ancho/2
    lead_y = display_alto/2

    lead_x_cambio = 0
    lead_y_cambio = 0

    listaSerp = []
    largoSerp = 1

    #Para que la manzana salga al azar
    AzManX = round(random.randrange(0, display_ancho-bloque_tamano))#)/10.0)*10.0
    AzManY = round(random.randrange(0, display_alto-bloque_tamano))#/10.0)*10.0

    #eventos
    while not gameExit:

        while gameOver == True:
            superficie.blit(imagen_redimensionada2, [0,0])
            message_to_screen("Game Over", rojo, -50, TamLet= "mediano")
            message_to_screen("Precione C para continuar y Q para terminar", blanco, 50, TamLet="pequeno")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_c:
                        gameLoop()
       


        for event in pygame.event.get():
            #cierra la ventana si se da a salir
            if event.type == pygame.QUIT:
                gameExit = True
            #definimos los movimientos izquierda/derecha
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_LEFT:
                    lead_x_cambio = -bloque_tamano
                    lead_y_cambio = 0 
                elif event.key ==pygame.K_RIGHT:
                    lead_x_cambio = bloque_tamano
                    lead_y_cambio = 0
                elif event.key ==pygame.K_UP:
                    lead_y_cambio = -bloque_tamano
                    lead_x_cambio = 0
                elif event.key ==pygame.K_DOWN:
                    lead_y_cambio = bloque_tamano
                    lead_x_cambio = 0
                elif event.key ==pygame.K_p:
                    pausa()


        #definimos los limites del juego
        if lead_x >= display_ancho or lead_x < 0 or lead_y >= display_alto or lead_y <0:
            gameOver=True

        lead_x +=lead_x_cambio 
        lead_y +=lead_y_cambio

        #hace una superficie al fondo del juego
        superficie.blit(imagen_redimensionada3, [0,0])
        tamanoMan = 20

        #dibujamos la manzana
        pygame.draw.rect(superficie, rojo, [AzManX,AzManY,tamanoMan,tamanoMan])
        
        CabezaSerp = []
        CabezaSerp.append(lead_x)
        CabezaSerp.append(lead_y)
        listaSerp.append(CabezaSerp)

        if len(listaSerp) > largoSerp:
            del listaSerp[0]

        #analiza todos los segmentos
        for eachSegment in listaSerp[:-1]:
            if eachSegment == CabezaSerp:
                gameOver = True

        #llamamos la serpiente
        serpiente(bloque_tamano,listaSerp)
        puntos(largoSerp-1)

        pygame.display.update()

#        if lead_x == AzManX and lead_y == AzManY:
#            AzManX = round(random.randrange(0, display_ancho-bloque_tamano)/10.0)*10.0
#            AzManY = round(random.randrange(0, display_alto-bloque_tamano)/10.0)*10.0
#            largoSerp += 1

        if lead_x >= AzManX and lead_x <= AzManX + tamanoMan:
            if lead_y >= AzManY and lead_y <= AzManY + tamanoMan:
                AzManX = round(random.randrange(0, display_ancho-bloque_tamano))#/10.0)*10.0
                AzManY = round(random.randrange(0, display_alto-bloque_tamano))#/10.0)*10.0
                largoSerp += 1 #Crecera la serpiente cada manzana que coma

        reloj.tick(FPS)
    pygame.quit()
    quit()



intro_juego()
gameLoop()




import pygame
from pygame.locals import *
import sys #Importa sistema para usar el cierre de ventana

pygame.init()

pantalla = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Hola Mundo")

rojo = 0
direccion = 1

#hacer que haga el bucle solo 3 veces
juego_activo = True
while juego_activo:
    for event in pygame.event.get():
        if event.type == QUIT:
           juego_activo = False
            
    if rojo >=255:
        direccion = -1
    if rojo <= 0:
        direccion = 1

    rojo += direccion

    pantalla.fill((rojo, 0, 0))

    pygame.display.flip()
    pygame.time.delay( 10 )


pygame.quit()
sys.exit()
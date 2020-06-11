import pygame as pg
from pygame.locals import *
import sys, random

BACKGROUND = (50,50,50)
YELLOW = (255, 255, 0)  
WHITE = (255, 255, 255)

WIN_GAME_SCORE = 10
'''
class movil(self, Ball, something):
    def __init__(self):
'''
class Ball: 
    def __init__(self):
        self.reset()
        self.h = 20 # ancho
        self.w = 20 # largo

        self.image = pg.Surface((self.w, self.h)) # carga la imagen de la bola
        self.image.fill(YELLOW) # da color a la imagen
        self.ping = pg.mixer.Sound('./resources/sounds/ping.wav') # le da sonido al punto
        self.lost_point = pg.mixer.Sound('./resources/sounds/lost-point.wav') # le pone sonido al golpe en cualquier pared

    @property
    def posx(self):
        return self.Cx - self.w // 2
        
    @property
    def posy(self):
        return self.Cy - self.h // 2

    def move(self, limSupX, limSupY): # da movimiento a la bola
        if self.Cx >= limSupX or self.Cx <=0: 
            self.vx = 0 # pone a cero la velocidad
            self.vy = 0
            self.lost_point.play() # activa sonido de toque a las paredes

        if self.Cy >= limSupY or self.Cy <=0:
            self.vy *= -1 # hace retroceder la bola cambiando la velocidad al contrario
            self.ping.play()
                
        self.Cx += self.vx # suma posicion x a velocidad x
        self.Cy += self.vy

    def comprobarChoque(self, something):
        dx = abs(self.Cx - something.Cx) # crea variable para comprobar el choque
        dy = abs(self.Cy - something.Cy) 

        if dx < (self.w + something.w)//2 and dy < (self.h +something.h) // 2: # formula para comprobar choque
            self.vx *= -1 # al haber choque cambia la velocidad al contrario
            self.Cx += self.vx # aumenta velocidad en la posicion
            self.Cy += self.vy
            self.ping.play() # sonido de punto

    def reset(self): # para comenzar si hay punto
        self.vx = random.choice([-7, -5, 5, 7])
        self.vy = random.choice([-7, -5, 5, 7]) 
        self.Cx = 400
        self.Cy = 300

class Raquet:
    def __init__(self, Cx):
        self.vx = 0
        self.vy = 0
        self.w = 25
        self.h = 100
        self.Cx = Cx
        self.Cy = 300

        self.image = pg.Surface((self.w, self.h)) #carga la raqueta
        self.image.fill((255, 255, 255)) #da color a la raqueta cargada

    @property
    def posx(self):
        return self.Cx - self.w // 2
        
    @property
    def posy(self):
        return self.Cy - self.h // 2

    def move(self, limSupX, limSupY):
        self.Cx += self.vx
        self.Cy += self.vy

        if self.Cy < self.h //2:
            self.Cy = self.h // 2

        if self.Cy > limSupY - self.h // 2:
            self.Cy = limSupY - self.h // 2        

class Game:
    def __init__(self):
        self.pantalla = pg.display.set_mode((800, 600))
        self.pantalla.fill(BACKGROUND)
        self.fondo = pg.image.load("./resources/images/fondo.jpg")
        self.ball = Ball()
        self.playerOne = Raquet(30)
        self.playerTwo = Raquet(770)

        self.status = 'Partida'

        self.font = pg.font.Font('./resources/font/font.ttf', 40)
        self.fontGrande = pg.font.Font('./resources/font/font.ttf', 60)

        self.marcadorOne = self.font.render("0", True, WHITE)
        self.marcadorTwo = self.font.render("0", True, WHITE)

        self.text_game_over = self.fontGrande.render("GAME OVER", True, YELLOW)
        self.text_insert_coin = self.font.render('<SPACE> - Inicio partida', True, WHITE)

        self.scoreOne = 0
        self.scoreTwo = 0
        pg.display.set_caption("Pong")

    def handlenEvent(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.quit()
            '''
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.playerOne.vy = -5
                if event.key == K_DOWN:
                    self.playerOne.vy = 5
            '''
        key_pressed = pg.key.get_pressed()
        if key_pressed[K_UP]:
            self.playerTwo.vy = - 5
        elif key_pressed[K_DOWN]:
            self.playerTwo.vy = 5
        else:
            self.playerTwo.vy = 0

        if key_pressed[K_w]:
            self.playerOne.vy = - 5
        elif key_pressed[K_z]:
            self.playerOne.vy = 5
        else:
            self.playerOne.vy = 0
        
        return False

    def bucle_partida(self):
        game_over = False
        self.scoreOne = 0
        self.scoreTwo = 0
        self.marcadorOne = self.font.render(str(self.scoreOne), True, WHITE)
        self.marcadorTwo = self.font.render(str(self.scoreOne), True, WHITE)

        while not game_over:
            game_over = self.handlenEvent()

            self.ball.move(800, 600)
            self.playerOne.move(800, 600)
            self.playerTwo.move(800, 600)
            self.ball.comprobarChoque(self.playerOne)
            self.ball.comprobarChoque(self.playerTwo)

            if self.ball.vx == 0 and self.ball.vy == 0:
                if self.ball.Cx >=800:
                    self.scoreOne += 1
                    self.marcadorOne = self.font.render(str(self.scoreOne), True, WHITE)
                if self.ball.Cx <= 0:
                    self.scoreTwo += 1
                    self.marcadorTwo = self.font.render(str(self.scoreTwo), True, WHITE)

                if self.scoreOne == WIN_GAME_SCORE or self.scoreTwo == WIN_GAME_SCORE:
                    game_over = True

                self.ball.reset()

            self.pantalla.blit(self.fondo, (0, 0))
            self.pantalla.blit(self.ball.image, (self.ball.posx, self.ball.posy))
            self.pantalla.blit(self.playerOne.image, (self.playerOne.posx, self.playerOne.posy))
            self.pantalla.blit(self.playerTwo.image, (self.playerTwo.posx, self.playerTwo.posy))
            self.pantalla.blit(self.marcadorOne, (30, 10))
            self.pantalla.blit(self.marcadorTwo, (740, 10))

            pg.display.flip()

        self.status = 'Inicio'

    def bucle_inicio(self):
        inicio_partida = False
        while not inicio_partida:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        inicio_partida = True

            self.pantalla.fill((0,0, 255))
            self.pantalla.blit(self.text_game_over, (100, 100))
            self.pantalla.blit(self.text_insert_coin, (100, 200))     

            pg.display.flip()       

        self.status = 'Partida'


    def main_loop(self):

        while True:
            if self.status == 'Partida':
                self.bucle_partida()
            else:
                self.bucle_inicio()


    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.main_loop()
    game.quit()
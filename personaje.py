
import pygame
import math



class Personaje():
    def __init__(self, x, y, animaciones, energia, tipo):
        self.score = 0
        self.energia = energia
        self.vivo  = True
        self.flip = False
        self.animaciones = animaciones
        #imagen de la animacion que se va a mostrar
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.shape = self.image.get_rect()
        self.shape.topleft = (x, y)
        self.tipo = tipo
        self.distancia = 200
        self.direccion = 1
        self.patrulla_distancia = 100
        self.patrulla_inicio = x
        self.velocidad = 1
        

        


    def draw(self, screen, scroll=(0,0)):
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(image_flip, (self.shape.x - scroll[0], self.shape.y - scroll[1]))
        #pygame.draw.rect(screen, (255, 255, 255), self.shape, width=1)





    def update(self, jugador=None, obstaculos=None):
        #comprobar el personaje ha muert
        if self.energia <=0:
            self.energia = 0
            self.vivo = False
         
    


        if self.tipo == 2 and jugador:

            dx = jugador.shape.centerx - self.shape.centerx
            dy = jugador.shape.centery - self.shape.centery

            distancia = math.sqrt(dx**2 + dy**2)

            if distancia < self.distancia:
                
                if dx > 0:
                    self.shape.x += 1
                if dx < 0:
                    self.shape.x -= 1
                if dy > 0:
                    self.shape.y += 1
                if dy < 0:
                    self.shape.y -= 1
            else:
                self.shape.x += self.direccion * self.velocidad
                if abs(self.shape.x - self.patrulla_inicio) > self.patrulla_distancia:
                        self.direccion *= -1
            if obstaculos:
                for tile in obstaculos:
                    if tile[1].colliderect(self.shape):
                        if dx > 0:
                                self.shape.right = tile[1].left
                        if dx < 0:
                                self.shape.left = tile[1].right
                        if dy > 0:
                                self.shape.bottom = tile[1].top     
                        if dy < 0:
                                self.shape.top = tile[1].bottom

                
    

      
        animation_cooldown = 100
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0

    def movimiento(self, delta_x, delta_y, width):
        posicion_pantalla = [0, 0]
        self.shape.x = self.shape.x + delta_x
        self.shape.y = self.shape.y + delta_y
        if   delta_x < 0:
            self.flip = True
        elif delta_x > 0:
            self.flip = False

        #logica para el jugador
        if self.tipo == 1:

         #mover la camara
            if self.shape.right > width - 200:
                posicion_pantalla[0] += self.shape.right - (width - 200)
            if self.shape.left < 200:
                posicion_pantalla[0] += self.shape.left - 200
        return posicion_pantalla
        


 
import pygame
import math
import random


class Weapon():
    def __init__(self, image, imagen_bala):
        self.imagen_bala = imagen_bala
        self.image_original = image
        self.angulo = 0
        self.image = pygame.transform.rotate(self.image_original, self.angulo)
        self.shape = self.image.get_rect()
        self.dispara = False
        self.ultimo_disparo = pygame.time.get_ticks()

    def update(self, jugador):
        disparo_cooldown = 500
        bala = None
        self.shape.center = jugador.shape.center
        if jugador.flip == False:
           self.shape.x = self.shape.x + jugador.shape.width//6
           self.rotar_arma (False)
        if jugador.flip == True:
           self.shape.x = self.shape.x - jugador.shape.width//6
           self.rotar_arma(True)
          
   #mover la pistola con el mouse
        mouse_pos = pygame.mouse.get_pos()
        distancia_x = mouse_pos[0] - self.shape.centerx
        distancia_y = -(mouse_pos[1] - self.shape.centery)
        self.angulo = math.degrees(math.atan2(distancia_y, distancia_x))

    #detectar los clicls del mouse para disparar
        if pygame.mouse.get_pressed()[0] and  self.dispara == False and pygame.time.get_ticks() - self.ultimo_disparo > disparo_cooldown:
            bala = Bullet(self.shape.centerx, self.shape.centery, self.angulo, self.imagen_bala) 
            self.dispara = True
            self.ultimo_disparo = pygame.time.get_ticks()

         #resetear el click del mouse 
        if  pygame.mouse.get_pressed()[0] == False:
            self.dispara = False
        return bala

    def rotar_arma(self, rotar):
        if rotar == True:
            imagen_flip = pygame.transform.flip(self.image_original, True, False)
            self.image = pygame.transform.rotate(self.image_original, self.angulo)
        else: imagen_flip = pygame.transform.flip(self.image_original, False, False)
        self.image = pygame.transform.rotate(imagen_flip, self.angulo)
    def draw(self, screen):
        screen.blit(self.image, self.shape)
       # pygame.draw.rect(screen, (255, 255, 255), self.shape, width=1)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, image):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        escala = 0.3
        ancho = int(image.get_width() * escala)
        alto = int(image.get_height() * escala)
        image = pygame.transform.scale(image, (ancho, alto))
        self.imagen_original = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
       
    #calculo de la velocidad de la bala
        velocidad = 10
        self.velocidad_x = math.cos(math.radians(self.angulo)) * velocidad//1.5
        self.velocidad_y = -math.sin(math.radians(self.angulo)) * velocidad//1.5

    def update(self, lista_enemigos):
            damage = 0
            pos_damage = None
            self.rect.x = self.rect.x + self.velocidad_x
            self.rect.y = self.rect.y + self.velocidad_y

            if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
                self.kill()   

        #verificar colosion enemigos
            for enemigo in lista_enemigos:
                if enemigo.shape.colliderect(self.rect):
                    damage = 15 + random.randint(-7, 7)
                    pos_damage = enemigo.shape
                    enemigo.energia = enemigo.energia - damage
                    self.kill()
                    break
            return damage, pos_damage
      
                    

    def draw(self, screen):
        screen.blit(self.image, (self.rect.centerx, self.rect.centery -int(self.image.get_height())/1.9))       

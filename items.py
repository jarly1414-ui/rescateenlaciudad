import pygame.sprite

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animacion_list, activo=True):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type # 0 = monedas, 1 = posiones
        self.animacion_list = animacion_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.activo = activo
        self.image = self.animacion_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center= (x, y)
        

    def update(self,jugador):
        #comprobar la colision
        if self.rect.colliderect(jugador.shape):
            #monedas
            if self.item_type == 0:
                jugador.score += 1
            #posiones
            if self.item_type == 1:
                jugador.energia += 20
                if jugador.energia > 100:
                    jugador.energia = 100   
                self.activo = False





        cooldown_animacion = 100
        self.image = self.animacion_list[self.frame_index]

        if pygame.time.get_ticks() - self.update_time > cooldown_animacion:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animacion_list):
            self.frame_index = 0    

    def draw(self, screen):
        screen.blit(self.image, self.rect)
import pygame
import sys
from personaje import Personaje
from weapons import Weapon
import os
from textos import DamageText
from items import Item
from mundo import Mundo
import csv
import behavior_tree

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width = screen.get_width() 
height = screen.get_height()
pygame.display.set_caption("RESCATE EN LA CIUDAD")

posicion_pantalla = [0, 0]

#fuentes
font = pygame.font.Font("assets/fonts/monogram.ttf", 25)
tile_size = 16  #tamano de cada tile del grid



def escalar_imagen(image, scale):
    new_width = int(image.get_width() * scale)
    new_height = int(image.get_height() * scale)
    return pygame.transform.scale(image, (new_width, new_height))

#energia
corazon_vacio = pygame.image.load("assets\images\items\heart_3.png")
corazon_vacio = escalar_imagen(corazon_vacio, 0.07)
corazon_mitad = pygame.image.load("assets\images\items\heart_2.png")
corazon_mitad = escalar_imagen(corazon_mitad, 0.07) 
corazon_lleno = pygame.image.load("assets\images\items\heart_1.png")
corazon_lleno = escalar_imagen(corazon_lleno, 0.07)

#funcion para contar elementos 
def contar_elementos(carpeta):
    return len(os.listdir(carpeta))



#funcion listar nombres elementos
def nombres_carpeta(carpeta):
    return os.listdir(carpeta)

(nombres_carpeta("assets/images/characters/player/player/enemies"))






animaciones = []
for i in range(7):
    img = pygame.image.load(f"assets\images\characters\player\player\player_{i}.png") 
    img = escalar_imagen(img, 0.5)
    animaciones.append(img)

#enemigos
directorio_enemigos = "assets/images/characters/player/player/enemies" 
tipo_enemigos = nombres_carpeta(directorio_enemigos)
animaciones_enemigos = []
for eni in tipo_enemigos: 
    lista_tem = []
    ruta_temp = f'assets/images/characters/player/player/enemies/{eni}'
    num_animaciones = contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        img_enemigo = pygame.image.load(f"{ruta_temp}//{eni}_{i + 1}.png")
        img_enemigo = escalar_imagen(img_enemigo, 0.5)
        lista_tem.append(img_enemigo)
    animaciones_enemigos.append(lista_tem)

        



imagen_pistola = pygame.image.load("assets\images\weapons\gun.png")
imagen_pistola = escalar_imagen(imagen_pistola, 0.02)

imagen_balas = pygame.image.load("assets\images\weapons/bullet.png")
imagen_balas = escalar_imagen(imagen_balas, 0.02)

#imagenes del mundo
num_tiles = len(os.listdir("assets/images/tiles"))
tile_list = []
for x in range(1, 487):
   tile_image = [pygame.image.load(f'assets/images/tiles/tile_{x}.png')]
   tile_image = pygame.transform.scale(tile_image[0], (tile_size, tile_size))
   tile_list.append(tile_image)

#imagenes de los items
posion_azul = pygame.image.load("assets/images/items/potion.webp")
posion_azul = escalar_imagen(posion_azul, 0.07)


coin_images = []
ruta_img = "assets\images\items\coin"
num_coin_images = contar_elementos(ruta_img)
for i in range(num_coin_images):
    img = pygame.image.load(f'assets/images/items/coin/coin_{i + 1}.png')
    img = escalar_imagen(img, 1.5)
    coin_images.append(img)

player_image = pygame.image.load("assets\images\characters\player\player\player_0.png")
player_image = pygame.transform.scale(player_image, (player_image.get_width() * 1.8, player_image.get_height() * 1.8))



#variables de movimiento
mover_arriba = False
mover_abajo = False
mover_izquierda = False 
mover_derecha = False

reloj = pygame.time.Clock()

def dibujar_texto(texto, font, color, x, y):
    img = font.render(texto, True, color)
    screen.blit(img, (x, y))

def vida_jugador():
    c_mitad_dibujada = False
    for i in range(3):
        if jugador.energia >= ((i + 1) * 33):
            screen.blit(corazon_lleno, (10 + i * 40, 10))
        elif jugador.energia >= ((i + 1) * 33) - 16 and c_mitad_dibujada == False:
            screen.blit(corazon_mitad, (10 + i * 40, 10))
            c_mitad_dibujada = True
        else:
            screen.blit(corazon_vacio, (10 + i * 40, 10))



filas = 60
columnas = 100

world_data = []

for fila in range(filas):
    r = [-1] * columnas
    world_data.append(r)

world_decor = []
for fila in range(filas):
    r = [-1] * columnas
    world_decor.append(r)

with open ("assets/niveles/mundo_decoraciones.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            world_decor[x][y] = int(columna)   

#cargar archivo csv
with open ("assets/niveles/mundo_suelo_suelo.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            world_data[x][y] = int(columna)

world = Mundo()
world.process_data(world_data, tile_list, tile_size, animaciones_enemigos)
world_decoraciones = Mundo()
world_decoraciones.process_data(world_decor, tile_list, tile_size, animaciones_enemigos)






#funcion para dibujar el grid
def dibujar_grid():
    for x in range(0, width, tile_size):
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, height))

    for y in range(0, height, tile_size):
        pygame.draw.line(screen, (255, 255, 255), (0, y), (width, y))



jugador = Personaje(width // 5, height // 2.5, animaciones, energia=100, tipo=1)



#crear lista de enemigos
lista_enemigos = world.lista_enemigos



#crear el arma del jugador
pistola = Weapon(imagen_pistola, imagen_balas)

#grupo de sprites
grupo_balas = pygame.sprite.Group()
grupo_damage_texts = pygame.sprite.Group()



items = []
items.append(Item(5 * tile_size + tile_size // 2, 4 * tile_size, 0, coin_images))
items.append(Item(6 * tile_size + tile_size // 2, 4 * tile_size, 0, coin_images))
items.append(Item(7 * tile_size + tile_size // 2, 4 * tile_size, 0, coin_images))

items.append(Item(10 * tile_size + tile_size // 2, 4 * tile_size, 1, [posion_azul]))
items.append(Item(11 * tile_size + tile_size // 2, 4 * tile_size, 1, [posion_azul]))





run = True
estado_juego = "menu"
pausa = False
while run:
   
    reloj.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if estado_juego == "menu" and event.key == pygame.K_RETURN:
                estado_juego = "jugando"
            
            if estado_juego == "game_over" and event.key == pygame.K_RETURN:
                run = False
            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == pygame.K_m:
                pygame.display.iconify()   
            
            if event.key == pygame.K_p:
                pausa = not pausa 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True  

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False  
    screen.fill((0,0,20))
    if estado_juego == "menu":
        screen.fill((0,0,0))
        dibujar_texto("RESCATE EN LA CIUDAD", font, (255, 255, 255), width // 2 - 150, height // 2 - 50)
        dibujar_texto("PRESIONA ENTER PARA INICIAR", font, (255, 255, 255), width // 2 - 150, height // 2)
          
        pygame.display.update()
        continue

    if estado_juego == "game_over":
        screen.fill((0,0,0))
        dibujar_texto("GAME OVER", font, (255, 255, 255), width // 2 - 100, height // 2 - 50)
        dibujar_texto(f'SCORE: {jugador.score}', font, (255, 255, 255), width // 2 - 100, height // 2)
        dibujar_texto("PRESIONA ENTER PARA REINICIAR", font, (255, 255, 255), width // 2 - 150, height // 2 + 50)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            run = False

        pygame.display.update()
        continue
    if pausa:
        dibujar_texto("PAUSA", font, (255,255,255),width//2, height //2)
        pygame.display.update()
        continue
    #dibujar_grid()


     


    delta_x = 0
    delta_y = 0

    if mover_arriba:
        delta_y -= 5
    if mover_abajo:
        delta_y += 5
    if mover_izquierda:
        delta_x -= 5
    if mover_derecha:
        delta_x += 5

    #dibujar mundo
    world.draw(screen, posicion_pantalla)
     #actualizar estado enemigo
    for enemigo in world.lista_enemigos:
        enemigo.update(jugador)
        enemigo.draw(screen, posicion_pantalla)

    world_decoraciones.draw(screen, posicion_pantalla)

    posicion_pantalla = jugador.movimiento(delta_x, delta_y, width)
    jugador.draw(screen, posicion_pantalla)
    jugador.update()
    if not jugador.vivo:
        estado_juego = "game_over"
    
    

    for item in items[:]:
        item.draw(screen)
    for item in items:
        item.update(jugador)

        if not item.activo:
            items.remove(item)

        

    bala = pistola.update(jugador)
    if bala:
        grupo_balas.add(bala)
    for bala in grupo_balas:
        damage, pos_damage = bala.update(world.lista_enemigos)
        if damage > 0 and pos_damage:
            damage_text = DamageText(pos_damage.centerx, pos_damage.y, str(damage), font, (255, 0, 0))
            grupo_damage_texts.add(damage_text)

    pistola.draw(screen)

    grupo_balas.update(world.lista_enemigos)
    
    #actualizar dano
    grupo_damage_texts.update()
    grupo_damage_texts.draw(screen)
    dibujar_texto(f'SCORE: {jugador.score}', font, (255, 255, 255), 10, 50)


    #dibujar balas 
    for bala in grupo_balas:
        bala.draw(screen)

    #dibujar vida jugador
    vida_jugador()    

    pygame.display.update()

pygame.quit()
sys.exit()

        
        

        

            


    
            


    
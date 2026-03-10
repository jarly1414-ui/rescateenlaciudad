from items import Item
from personaje import Personaje

class Mundo():
    def __init__(self):
        self.map_tiles = []
        self.lista_enemigos = []

    def process_data(self, data, tiles_list, tile_size, animaciones_enemigos):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                #crear enemigo gobin
                if tile == 307:

                    gobin = Personaje(x * tile_size, y * tile_size, animaciones_enemigos[0], energia=100, tipo=2)
                    self.lista_enemigos.append(gobin)
                    imagen = tiles_list[461]
                    imagen_rect = imagen.get_rect()
                    imagen_rect.x = x * tile_size
                    imagen_rect.y = y * tile_size
                    tile_data = (imagen, imagen_rect)
                    self.map_tiles.append(tile_data)
                    

                    
                    #crear enemigo blue
                elif tile == 252:
                    blue = Personaje(x * tile_size, y * tile_size, animaciones_enemigos[1], energia=100, tipo=2)
                    self.lista_enemigos.append(blue)
                    imagen = tiles_list[461]
                    imagen_rect = imagen.get_rect()     
                    imagen_rect.x = x * tile_size
                    imagen_rect.y = y * tile_size
                    tile_data = (imagen, imagen_rect)
                    self.map_tiles.append(tile_data)
                    
                
                elif tile >= 0:

                    image = tiles_list[tile]
                    image_rect = image.get_rect()   
                    image_rect.x = x * tile_size
                    image_rect.y = y * tile_size 
                    tile_data = (image, image_rect)
                    self.map_tiles.append(tile_data)
                    
                
                    



    def draw(self, surface, scroll):  
        for tile in self.map_tiles:
            surface.blit(tile[0], (tile[1].x - scroll[0], tile[1].y - scroll[1]))           
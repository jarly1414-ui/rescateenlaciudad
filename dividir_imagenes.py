from PIL import Image
import os

def dividir_tiles(ruta_imagen, carpeta_destino, tile_size):
    img = Image.open(ruta_imagen)
    ancho, alto = img.size 

    columnas = ancho // tile_size
    filas = alto // tile_size

    os.makedirs(carpeta_destino, exist_ok=True)
    contador = 1

    for y in range(filas):
        for x in range(columnas):
            izquierda = x * tile_size
            superior = y * tile_size
            derecha = izquierda + tile_size
            inferior = superior + tile_size

            tile = img.crop((izquierda, superior, derecha, inferior))
            tile.save(f'{carpeta_destino}/tile_{contador}.png')
            contador += 1

dividir_tiles(
    "assets/images/tiles/tilemap_packed.png", 
    "assets/images/tiles", 
    16
)           


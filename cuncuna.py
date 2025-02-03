import pygame
import time
import random

# Inicializar pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Tamaño de la pantalla
ANCHO = 600
ALTO = 400

# Tamaño de cada segmento de la serpiente y velocidad
TAMANO_SEGMENTO = 20
VELOCIDAD = 15

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de la Cuncuna (Serpiente)")

# Reloj para controlar la velocidad del juego
reloj = pygame.time.Clock()

# Fuente para mostrar el puntaje
fuente = pygame.font.SysFont("Arial", 25)

def mostrar_puntaje(puntaje):
    texto = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
    pantalla.blit(texto, [10, 10])

def dibujar_serpiente(tamano_segmento, lista_serpiente):
    for segmento in lista_serpiente:
        pygame.draw.rect(pantalla, VERDE, [segmento[0], segmento[1], tamano_segmento, tamano_segmento])

def juego():
    game_over = False
    game_cerrado = False

    # Posición inicial de la serpiente
    x = ANCHO / 2
    y = ALTO / 2

    # Cambio en la posición
    cambio_x = 0
    cambio_y = 0

    # Lista de la serpiente
    lista_serpiente = []
    largo_serpiente = 1

    # Posición de la comida
    comida_x = round(random.randrange(0, ANCHO - TAMANO_SEGMENTO) / TAMANO_SEGMENTO) * TAMANO_SEGMENTO
    comida_y = round(random.randrange(0, ALTO - TAMANO_SEGMENTO) / TAMANO_SEGMENTO) * TAMANO_SEGMENTO

    while not game_over:
        while game_cerrado:
            pantalla.fill(NEGRO)
            texto = fuente.render("¡Perdiste! Presiona Q para salir o C para jugar de nuevo", True, BLANCO)
            pantalla.blit(texto, [ANCHO / 6, ALTO / 3])
            mostrar_puntaje(largo_serpiente - 1)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        game_over = True
                        game_cerrado = False
                    if evento.key == pygame.K_c:
                        juego()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and cambio_x == 0:
                    cambio_x = -TAMANO_SEGMENTO
                    cambio_y = 0
                elif evento.key == pygame.K_RIGHT and cambio_x == 0:
                    cambio_x = TAMANO_SEGMENTO
                    cambio_y = 0
                elif evento.key == pygame.K_UP and cambio_y == 0:
                    cambio_y = -TAMANO_SEGMENTO
                    cambio_x = 0
                elif evento.key == pygame.K_DOWN and cambio_y == 0:
                    cambio_y = TAMANO_SEGMENTO
                    cambio_x = 0

        # Si la serpiente choca con los bordes, termina el juego
        if x >= ANCHO or x < 0 or y >= ALTO or y < 0:
            game_cerrado = True

        x += cambio_x
        y += cambio_y
        pantalla.fill(NEGRO)
        pygame.draw.rect(pantalla, ROJO, [comida_x, comida_y, TAMANO_SEGMENTO, TAMANO_SEGMENTO])

        # Añadir la nueva cabeza de la serpiente
        cabeza_serpiente = [x, y]
        lista_serpiente.append(cabeza_serpiente)

        if len(lista_serpiente) > largo_serpiente:
            del lista_serpiente[0]

        # Si la serpiente choca consigo misma, termina el juego
        for segmento in lista_serpiente[:-1]:
            if segmento == cabeza_serpiente:
                game_cerrado = True

        dibujar_serpiente(TAMANO_SEGMENTO, lista_serpiente)
        mostrar_puntaje(largo_serpiente - 1)

        pygame.display.update()

        # Si la serpiente come la comida
        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, ANCHO - TAMANO_SEGMENTO) / TAMANO_SEGMENTO) * TAMANO_SEGMENTO
            comida_y = round(random.randrange(0, ALTO - TAMANO_SEGMENTO) / TAMANO_SEGMENTO) * TAMANO_SEGMENTO
            largo_serpiente += 1
            global VELOCIDAD
            VELOCIDAD += 1  # Aumentar la velocidad

        reloj.tick(VELOCIDAD)

    pygame.quit()
    quit()

# Iniciar el juego
juego()
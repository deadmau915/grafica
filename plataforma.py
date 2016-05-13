import pygame
from libplataforma import *

#http://collabedit.com/abvtc

class Plataforma(pygame.sprite.Sprite):
    """ Plataforma donde el usuario puede subir """
    
    def __init__(self, ancho, alto):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([ancho, alto])
        self.image.fill(VERDE)
        
        self.rect = self.image.get_rect()


class Nivel(object):
    """ Esta es una superclase usada para definir un nivel
        Se crean clases hijas por cada nivel que desee emplearse """
    
    # Lista de sprites usada en todos los niveles. Add or remove
    plataforma_lista = None
    enemigos_lista = None
    
    # Imagen de Fondo
    #fondo = None
    fondo=pygame.image.load("espacio.jpg")
    #valor desplazamiento de fondo
    mov_fondo=0
    
    def __init__(self, jugador):
        self.plataforma_lista = pygame.sprite.Group()
        self.enemigos_lista = pygame.sprite.Group()
        self.jugador = jugador
    
    # Actualizamos elementos en el nivel
    def update(self):
        """ Actualiza todo lo que este en este nivel."""
        self.plataforma_lista.update()
        self.enemigos_lista.update()
    
    def draw(self, pantalla):
        """ Dibuja lo que se encuentre en el nivel. """
        
        # Dibujamos fondo
        pantalla.fill(AZUL)
        
        pantalla.blit(self.fondo, (0,0))
        
        # Dibujamos todos los sprites en las listas
        self.plataforma_lista.draw(pantalla)
        self.enemigos_lista.draw(pantalla)

    def Mover_fondo(self, mov_x):
        self.mov_fondo += mov_x
        for plataforma in self.plataforma_lista:
            plataforma.rect.x += mov_x
        for enemigo in self.enemigos_lista:
            enemigo.rect.x += mov_x

class Nivel_02(Nivel):
    """ Definicion para el nivel 2. """
    
    def __init__(self, jugador):
        """ Creamos nivel 2. """
        
        # Llamamos al padre
        Nivel.__init__(self, jugador)
        self.limite=-1000
        # Arreglo con ancho, alto, x, y de la plataforma
        nivel = [ [210, 50, 500, 500],
                 [210, 50, 200, 400],
                 [210, 50, 1000, 520],
                 [210, 50, 1200, 300],
                 ]
            
        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.rect.x = plataforma[2]
            bloque.rect.y = plataforma[3]
            bloque.jugador = self.jugador
            self.plataforma_lista.add(bloque)

class Nivel_01(Nivel):
    """ Definition for level 1. """
    
    def __init__(self, jugador):
        """ Creamos nivel 1. """
        
        # Llamamos al padre
        Nivel.__init__(self, jugador)
        self.limite=-1000
        # Arreglo con ancho, alto, x, y de la plataforma
        nivel = [ [210, 70, 500, 500],
                  [210, 70, 800, 400],
                  [210, 70, 1000, 500],
                  [210, 70, 1120, 300],
                 ]
            
        
        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.rect.x = plataforma[2]
            bloque.rect.y = plataforma[3]
            self.plataforma_lista.add(bloque)


if __name__ == "__main__":
    """ Programa principal """
    pygame.init()
    tam = [ANCHO, ALTO]
    pantalla = pygame.display.set_mode(tam)
    
    pygame.display.set_caption("Ejemplo de juego de plataforma")
    
    # Creamos jugador
    jugador = Jugador()
    
    # Creamos los niveles
    nivel_lista = []
    nivel_lista.append( Nivel_01(jugador) )
    nivel_lista.append( Nivel_02(jugador) )
    
    # Establecemos nivel actual
    nivel_actual_no = 0
    nivel_actual = nivel_lista[nivel_actual_no]
    
    # Lista de sprites activos
    activos_sp_lista = pygame.sprite.Group()
    # Indicamos a la clase jugador cual es el nivel
    jugador.nivel = nivel_actual
    
    jugador.rect.x = 340
    jugador.rect.y = ALTO - jugador.rect.height
    activos_sp_lista.add(jugador)
    
    fin = False
    
    # Controlamos que tan rapido actualizamos pantalla
    reloj = pygame.time.Clock()
    
     # -------- Ciclo del juego -----------
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    jugador.ir_izq()
                if event.key == pygame.K_RIGHT:
                    jugador.ir_der()
                if event.key == pygame.K_UP:
                    print "salto"
                    jugador.salto()
        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and jugador.vel_x < 0:
                    jugador.no_mover()
                if event.key == pygame.K_RIGHT and jugador.vel_x > 0:
                    jugador.no_mover()
                    
        # Actualizamos al jugador.
        activos_sp_lista.update()
    
        # Actualizamos elementos en el nivel
        nivel_actual.update()
        
        #  Si el jugador se aproxima al limite derecho de la pantalla (-x)
        if jugador.rect.x >= 500:
            dif = jugador.rect.x - 500
            jugador.rect.x = 500
            nivel_actual.Mover_fondo(-dif)

        # Si el jugador se aproxima al limite izquierdo de la pantalla (+x)
        if jugador.rect.x <= 120:
           dif = 120 - jugador.rect.x
           jugador.rect.x = 120
           nivel_actual.Mover_fondo(dif)
           
        #Si llegamos al final del nivel
        pos_actual=jugador.rect.x + nivel_actual.mov_fondo
        if pos_actual < nivel_actual.limite:
           jugador.rect.x=120
           if nivel_actual_no < len(nivel_lista)-1:
              nivel_actual_no += 1
              nivel_actual = nivel_lista[nivel_actual_no]
              jugador.nivel=nivel_actual

        # Dibujamos y refrescamos
        
        nivel_actual.draw(pantalla)
        activos_sp_lista.draw(pantalla)
        reloj.tick(60)
        pygame.display.flip()

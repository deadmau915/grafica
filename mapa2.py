import pygame
from pygame.locals import *
import sys
import pygame.locals
import ConfigParser

ALTO = 576
ANCHO = 768

def cargar_fondo(archivo, ancho, alto):
    imagen = pygame.image.load(archivo).convert()
    imagen_ancho, imagen_alto = imagen.get_size()
    print imagen_ancho
    print imagen_alto
    tabla_fondos = []    
    for fondo_x in range(0, imagen_ancho/ancho):
       linea = []
       tabla_fondos.append(linea)
       for fondo_y in range(0, imagen_alto/alto):
            cuadro = (fondo_x * ancho, fondo_y * alto, ancho, alto)
            linea.append(imagen.subsurface(cuadro))
    return tabla_fondos 

class Nivel(object):
    def cargar_archivo(self, archivo="niveles.map"):
        self.mapa = []
        self.indice = {}
        interprete = ConfigParser.ConfigParser()
        interprete.read(archivo)
        self.grfondos = interprete.get("nivel1", "origen")
        self.mapa = interprete.get("nivel1", "mapa").split("\n")
        for seccion in interprete.sections():
            if len(seccion) == 1:
               print len(seccion)
               desc = dict(interprete.items(seccion))
               self.indice[seccion] = desc
        self.ancho = len(self.mapa[0])
        self.alto = len(self.mapa)
        print self.ancho, self.alto

    def tomar_fondo(self, x,y):
        """ Captura la posicion especifica en el mapa"""
        try:
            char = self.mapa[y][x]
        except IndexError:
            return {}
        try:
            lc = self.indice[char]
            #aqui esta el problema
            return lc
        except KeyError:
            return {}  

    def tomar_bool(self, x, y, tipod):
        """ Retorna el valor booleano de la posicion mapa"""
        valor = self.tomar_fondo(x, y)
        #print valor
        resultado=False
        #print valor[tipod], x, y        
        if valor[tipod] == "si" :
          resultado=True
        return resultado
  
    def es_muro(self, x, y):
        """ Es un muro?"""
        return self.tomar_bool(x, y, 'muro') 

    def es_bloque(self, x, y):
        """ Esta bloqueado?"""
        if not 0 <= x < self.ancho or not 0 <= y < self.alto:
           return True
        return self.tomar_bool(x, y, 'bloqueo') 

    def Dibujar(self):
        #extrae column fila al llamra el cuadro
        cuadro= 0, 0
        fondos = MAPA_REP[self.grfondos]
        imagen = pygame.Surface((self.ancho*FONDO_ANCHO, self.alto*FONDO_ALTO))
        for mx, linea in enumerate(self.mapa):
            print linea
            for my, cd in enumerate (linea):
                print mx, my
                if self.es_muro(my, mx):
                    cuadro= 8,6                    
                else:
                    cuadro= 0,0
                print cuadro
                img_fondo=fondos[cuadro[0]][cuadro[1]]
                imagen.blit(img_fondo, (my*FONDO_ALTO, mx*FONDO_ANCHO)) 
        return imagen
        

if __name__ == '__main__':
   pygame.init()
   pantalla = pygame.display.set_mode((ANCHO, ALTO))

   FONDO_ANCHO = 32
   FONDO_ALTO = 32
   MAPA_REP = {'terrenos.png':cargar_fondo('terrenos.png', FONDO_ANCHO, FONDO_ALTO), }
   pantalla.fill((255, 255, 255))
   #print MAPA_REP
   nivel= Nivel()   
   nivel.cargar_archivo('niveles.map')

   #nivel.Dibujar()
   fondo=nivel.Dibujar()
   pantalla.blit(fondo, (0,0))
   pygame.display.flip()
 
   while True:
      tecla = pygame.key.get_pressed()
      for event in pygame.event.get():
          if tecla[K_ESCAPE] or event.type == pygame.QUIT:
            raise SystemExit 

import pygame

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
"""Colores"""

LARGO_PANTALLA = 1000
ALTO_PANTALLA = 800
"""Dimensiones de la pantalla"""


class Protagonista(pygame.sprite.Sprite):
    cambio_x = 0
    cambio_y = 0
    nivel = None

    def __init__(self):
        """Define la carga de imagen del protagonista
        """
        super().__init__()

        self.walkingLeft = [pygame.image.load("L1.png"),
                            pygame.image.load("L2.png"),
                            pygame.image.load("L3.png"),
                            pygame.image.load("L4.png"),
                            pygame.image.load("L5.png"),
                            pygame.image.load("L6.png"),
                            pygame.image.load("L7.png"),
                            pygame.image.load("L8.png"),
                            pygame.image.load("L9.png")
                            ]
        self.walkingRight = [pygame.image.load("R1.png"),
                             pygame.image.load("R2.png"),
                             pygame.image.load("R3.png"),
                             pygame.image.load("R4.png"),
                             pygame.image.load("R5.png"),
                             pygame.image.load("R6.png"),
                             pygame.image.load("R7.png"),
                             pygame.image.load("R8.png"),
                             pygame.image.load("R9.png")
                             ]

        self.direction = "R"
        self.image = self.walkingRight[0]
        self.rect = self.image.get_rect()

    def update(self):
        """Actualiza el movimiento y animación del protagonista y
        comprueba colisiones con los objetos del nivel
        """
        self.calc_grav()
        self.rect.x += self.cambio_x
        pos = self.rect.x
        if self.direction == "R":
            frame = (pos // 27) % len(self.walkingRight)
            self.image = self.walkingRight[frame]
        else:
            frame = (pos // 27) % len(self.walkingLeft)
            self.image = self.walkingLeft[frame]

        lista_impactos_bloques = pygame.sprite.spritecollide(self,
                                                             self.nivel.listade_plataformas, False)

        for bloque in lista_impactos_bloques:
            if self.cambio_x > 0:
                self.rect.right = bloque.rect.left
            elif self.cambio_x < 0:
                self.rect.left = bloque.rect.right
        self.rect.y += self.cambio_y

        lista_impactos_bloques = pygame.sprite.spritecollide(self,
                                                             self.nivel.listade_plataformas, False)

        for bloque in lista_impactos_bloques:
            if self.cambio_y > 0:
                self.rect.bottom = bloque.rect.top
            elif self.cambio_y < 0:
                self.rect.top = bloque.rect.bottom
            self.cambio_y = 0

    def calc_grav(self):
        """ Permite calcular la gravedad dek protagonista
        """
        if self.cambio_y == 0:
            self.cambio_y = 1
        else:
            self.cambio_y += .35

        if self.rect.y >= ALTO_PANTALLA - self.rect.height and \
                self.cambio_y >= 0:
            self.cambio_y = 0
            self.rect.y = ALTO_PANTALLA - self.rect.height

    def saltar(self):
        """ Permite al protagonista saltar
        """
        self.rect.y += 2
        lista_impactos_plataforma = pygame.sprite.spritecollide(self,
                                                                self.nivel.listade_plataformas, False)
        self.rect.y -= 2

        if len(lista_impactos_plataforma) > 0 or \
                self.rect.bottom >= ALTO_PANTALLA:
            self.cambio_y = -8

    def ir_izquierda(self):
        """Permite al protagonista moverse a la izquierda
        """
        self.cambio_x = -6
        self.direction = "L"

    def ir_derecha(self):
        """Permite al protagonista moverse a la izquierda
        """
        self.cambio_x = 6
        self.direction = "R"

    def stop(self):
        """Permite al protagonista quedarse quieto
        """
        self.cambio_x = 0


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, largo, alto):
        """ Constructor de las plataformas donde se mueve el
        protagonista
        Args:
            largo (int): Largo de la plataforma
            alto (int): Alto de la plataforma
        """
        super().__init__()
        self.image = pygame.Surface([largo, alto])
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()


class PlataformaEnMovimiento(Plataforma):
    cambio_x = 0
    cambio_y = 0

    limite_superior = 0
    limite_inferior = 0
    limite_izquierda = 0
    limite_derecha = 0

    protagonista = None

    Nivel = None

    def update(self):
        """Actualiza el movimiento del protagonista sobre las
        plataformas móviles y comprueba las colisiones con las mismas
        """
        self.rect.x += self.cambio_x

        impacto = pygame.sprite.collide_rect(self, self.protagonista)
        if impacto:
            if self.cambio_x < 0:
                self.protagonista.rect.right = self.rect.left
            else:
                self.protagonista.rect.left = self.rect.right

        self.rect.y += self.cambio_y

        impacto = pygame.sprite.collide_rect(self, self.protagonista)
        if impacto:
            if self.cambio_y < 0:
                self.protagonista.rect.bottom = self.rect.top
            else:
                self.protagonista.rect.top = self.rect.bottom

        if self.rect.bottom > self.limite_inferior or \
                self.rect.top < self.limite_superior:
            self.cambio_y *= -1


class Nivel(object):
    def __init__(self, protagonista):
        """ Constructor requerido para cuando las plataformas
        móviles colisionan con el protagonista
        Args:
            protagonista (objeto): Contiene los atributos del
            protagonista
        """
        self.listade_plataformas = pygame.sprite.Group()
        self.protagonista = protagonista
        self.imagende_fondo = None

    def update(self):
        """ Actualiza las plataformas en el nivel
        """
        self.listade_plataformas.update()

    def draw(self, pantalla):
        """ Dibuja todo en el nivel
        Args:
            pantalla (pygame.display.set_mode): Crea la pantalla del
            juego con las dimensiones entregadas
        """
        pantalla.fill(AZUL)
        pantalla.blit(self.imagende_fondo, (0, 0))

        self.listade_plataformas.draw(pantalla)



class Nivel_01(Nivel):
    def __init__(self, protagonista):
        """Crea el nivel 1 con sus respectivas plataformas
        Args:
            protagonista (objeto): Contiene los atributos del
            protagonista
        """
        Nivel.__init__(self, protagonista)

        self.imagende_fondo = pygame.image.load("fondof.png").convert()

        nivel = [[500, 10, 0, 120],
                 [100, 10, 450, 330],
                 [100, 10, 270, 330],
                 [100, 10, 100, 420],
                 [100, 10, 270, 480],
                 [100, 10, 0, 550],
                 [600, 10, 200, 550],
                 [100, 10, 900, 550],
                 [450, 10, 0, 680],
                 [450, 10, 550, 680],
                 [1000, 1, 0, 0]
                 ]

        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.rect.x = plataforma[2]
            bloque.rect.y = plataforma[3]
            bloque.protagonista = self.protagonista
            self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 451
        bloque.rect.y = 710
        bloque.limite_superior = 710
        bloque.limite_inferior = 790
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 100
        bloque.rect.y = 590
        bloque.limite_superior = 590
        bloque.limite_inferior = 690
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 800
        bloque.rect.y = 560
        bloque.limite_superior = 560
        bloque.limite_inferior = 670
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 550
        bloque.rect.y = 90
        bloque.limite_superior = 90
        bloque.limite_inferior = 270
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)


class Nivel_02(Nivel):
    def __init__(self, protagonista):
        """Crea el nivel 2 con sus respectivas plataformas
        Args:
            protagonista (objeto): Contiene los atributos del
            protagonista
        """
        Nivel.__init__(self, protagonista)

        self.imagende_fondo = pygame.image.load("fondof.png").convert()

        nivel = [[200, 10, 0, 680],
                 [200, 10, 500, 680],
                 [400, 10, 100, 560],
                 [400, 10, 600, 560],
                 [900, 10, 0, 440],
                 [100, 10, 550, 220],
                 [100, 10, 700, 220],
                 [350, 10, 0, 120],
                 [1000, 1, 0, 0]
                 ]

        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.rect.x = plataforma[2]
            bloque.rect.y = plataforma[3]
            bloque.protagonista = self.protagonista
            self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 200
        bloque.rect.y = 680
        bloque.limite_superior = 680
        bloque.limite_inferior = 790
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 700
        bloque.rect.y = 680
        bloque.limite_superior = 680
        bloque.limite_inferior = 790
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 0
        bloque.rect.y = 560
        bloque.limite_superior = 560
        bloque.limite_inferior = 670
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 500
        bloque.rect.y = 560
        bloque.limite_superior = 560
        bloque.limite_inferior = 670
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 900
        bloque.rect.y = 440
        bloque.limite_superior = 440
        bloque.limite_inferior = 550
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 100
        bloque.rect.y = 340
        bloque.limite_superior = 340
        bloque.limite_inferior = 430
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 300
        bloque.rect.y = 260
        bloque.limite_superior = 260
        bloque.limite_inferior = 340
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 400
        bloque.rect.y = 100
        bloque.limite_superior = 100
        bloque.limite_inferior = 150
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)


class Nivel_03(Nivel):
    def __init__(self, protagonista):
        """Crea el nivel 3 con sus respectivas plataformas
        Args:
            protagonista (objeto): Contiene los atributos del
            protagonista
        """
        Nivel.__init__(self, protagonista)

        self.imagende_fondo = pygame.image.load("fondof.png").convert()

        nivel = [[450, 10, 0, 490],
                 [450, 10, 550, 490],
                 [100, 10, 50, 440],
                 [100, 10, 230, 370],
                 [100, 10, 400, 370],
                 [100, 10, 600, 370],
                 [100, 10, 800, 370],
                 [100, 10, 900, 300],
                 [100, 10, 780, 210],
                 [100, 10, 580, 210],
                 [300, 10, 0, 120],
                 [1000, 1, 0, 0]
                 ]

        for plataforma in nivel:
            bloque = Plataforma(plataforma[0], plataforma[1])
            bloque.rect.x = plataforma[2]
            bloque.rect.y = plataforma[3]
            bloque.protagonista = self.protagonista
            self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 800
        bloque.rect.y = 700
        bloque.limite_superior = 700
        bloque.limite_inferior = 790
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 600
        bloque.rect.y = 640
        bloque.limite_superior = 640
        bloque.limite_inferior = 700
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 450
        bloque.rect.y = 490
        bloque.limite_superior = 490
        bloque.limite_inferior = 630
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)

        bloque = PlataformaEnMovimiento(100, 10)
        bloque.rect.x = 400
        bloque.rect.y = 100
        bloque.limite_superior = 100
        bloque.limite_inferior = 180
        bloque.cambio_y = -1
        bloque.protagonista = self.protagonista
        bloque.nivel = self
        self.listade_plataformas.add(bloque)


def main():
    """Programa Principal
    """
    pygame.init()

    dimensiones = [LARGO_PANTALLA, ALTO_PANTALLA]
    pantalla = pygame.display.set_mode(dimensiones)

    pygame.display.set_caption("Donkey Konga")

    protagonista = Protagonista()

    listade_niveles = [Nivel_01(protagonista), Nivel_02(protagonista),
                       Nivel_03(protagonista)]

    nivel_actual_no = 0
    nivel_actual = listade_niveles[nivel_actual_no]

    lista_sprites_activos = pygame.sprite.Group()
    protagonista.nivel = nivel_actual

    protagonista.rect.x = 0
    protagonista.rect.y = ALTO_PANTALLA - protagonista.rect.height
    lista_sprites_activos.add(protagonista)

    hecho = False

    reloj = pygame.time.Clock()

    while not hecho:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                hecho = True

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    protagonista.ir_izquierda()
                if evento.key == pygame.K_RIGHT:
                    protagonista.ir_derecha()
                if evento.key == pygame.K_UP:
                    protagonista.saltar()

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT and protagonista.cambio_x < 0:
                    protagonista.stop()
                if evento.key == pygame.K_RIGHT and protagonista.cambio_x > 0:
                    protagonista.stop()

        lista_sprites_activos.update()

        nivel_actual.update()

        if protagonista.rect.right > LARGO_PANTALLA:
            protagonista.rect.right = LARGO_PANTALLA

        if protagonista.rect.left < 0:
            protagonista.rect.left = 0

        if protagonista.rect.x == 0 and protagonista.rect.y == 10:
            nivel_actual_no += 1
            nivel_actual = listade_niveles[nivel_actual_no]
            protagonista.nivel = nivel_actual
            protagonista.rect.x = 0
            protagonista.rect.y = ALTO_PANTALLA - protagonista.rect.height
            lista_sprites_activos.add(protagonista)

        nivel_actual.draw(pantalla)
        lista_sprites_activos.draw(pantalla)

        reloj.tick(60)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

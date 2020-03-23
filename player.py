import pygame as pg


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.speed = 10

    def draw(self, window):
        pg.draw.rect(window, self.color, self.rect)

    def move(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.x -= self.speed
        elif keys[pg.K_RIGHT]:
            self.x += self.speed
        if keys[pg.K_UP]:
            self.y -= self.speed
        elif keys[pg.K_DOWN]:
            self.y += self.speed
        if keys[pg.K_SPACE]:
            pass

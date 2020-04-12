import pygame as pg
import time


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, color):
        pg.sprite.Sprite.__init__(self)
        # self.image = pg.Surface((width, height))
        # self.image.fill(color)
        # self.rect = self.image.get_rect()
        # self.rect.center = (x+32, y+32)
        self.x = x
        self.y = y
        self.color = color
        self.width = 64
        self.height = 64
        self.rect = (x, y, self.width, self.height)
        self.speed = 10
        self.cd = 3
        self.last_cast = None

    def draw(self, window):
        pg.draw.rect(window, self.color, self.rect)

    def move(self, client):
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
            if self.last_cast is None:
                self.place_bomb(client)
            elif time.time() - self.last_cast > self.cd:
                self.place_bomb(client)

    def place_bomb(self, client):
        self.last_cast = time.time()
        client.dispatch_event(
            event_type="BOMB",
            player_id=client.player_id,
            position=(self.x, self.y)
        )

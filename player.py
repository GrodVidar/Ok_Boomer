import pygame as pg
import time


class Player:
    def __init__(self, x, y, color):
        self.color = color
        self.width = 50
        self.height = 50
        self.rect = pg.Rect(x, y, self.width, self.height)
        self.speed = 5
        self.cd = 3
        self.last_cast = None

    def move(self, client, walls):
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            if self.rect.x - self.speed >= 0 and not self.check_collision(walls, 'l'):
                self.rect.x -= self.speed
        elif keys[pg.K_RIGHT]:
            if self.rect.x + self.speed <= 526 and not self.check_collision(walls, 'r'):
                self.rect.x += self.speed
        if keys[pg.K_UP]:
            if self.rect.y - self.speed >= 0 and not self.check_collision(walls, 'u'):
                self.rect.y -= self.speed
        elif keys[pg.K_DOWN]:
            if self.rect.y + self.speed <= 526 and not self.check_collision(walls, 'd'):
                self.rect.y += self.speed
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
            position=self.rect.center
        )

    def check_collision(self, walls, dir):
        will_collide = False
        for i in walls:
            dummy = pg.Rect(self.rect)
            if dir == 'l':
                dummy.x -= self.speed
                if i.colliderect(dummy):
                    will_collide = True
            if dir == 'r':
                dummy.x += self.speed
                if i.colliderect(dummy):
                    will_collide = True
            if dir == 'u':
                dummy.y -= self.speed
                if i.colliderect(dummy):
                    will_collide = True
            if dir == 'd':
                dummy.y += self.speed
                if i.colliderect(dummy):
                    will_collide = True
        return will_collide

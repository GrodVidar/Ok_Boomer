import pygame as pg
import time


def get_bomb_spot(origin_x, origin_y):
    x = (int(origin_x/64)*64) + 32 - 10
    y = (int(origin_y/64)*64) + 32 - 10
    return x, y


class Player:
    def __init__(self, x, y, color, hp):
        self.color = color
        self.width = 50
        self.height = 50
        self.rect = pg.Rect(x, y, self.width, self.height)
        self.hp = hp
        self.speed = 5
        self.cd = 3
        self.last_cast = None

    def move(self, client, walls):
        keys = pg.key.get_pressed()
        if self.hp > 0:
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
        if self.hp > 0:
            self.last_cast = time.time()
            client.dispatch_event(
                event_type="BOMB",
                player_id=client.player_id,
                position=(get_bomb_spot(self.rect.centerx, self.rect.centery))
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

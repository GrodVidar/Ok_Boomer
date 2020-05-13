import pygame as pg
import time


# calculates the placement for the bomb the player places
# so that the bomb will be centered and not stuck inside of a wall.
def get_bomb_spot(origin_x, origin_y):
    x = (int(origin_x/64)*64) + 32 - 10
    y = (int(origin_y/64)*64) + 32 - 10
    return x, y


class Player:
    def __init__(self, x, y, player_id, hp):
        if player_id == 0:
            self.color = (50, 50, 255)
        elif player_id == 1:
            self.color = (50, 255, 50)
        elif player_id == 2:
            self.color = (255, 50, 50)
        elif player_id == 3:
            self.color = (255, 211, 25)
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

    # when the player presses space, this will trigger, which tells the server what player
    # and where the player places the bomb.
    def place_bomb(self, client):
        if self.hp > 0:
            self.last_cast = time.time()
            client.dispatch_event(
                event_type="BOMB",
                player_id=client.player_id,
                position=(get_bomb_spot(self.rect.centerx, self.rect.centery))
            )

    # method that checks if the player is going in a specific direction, if there is a wall
    # in its path, this will stop the player from walking into a wall.
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

from pygase import Client
import pygame as pg
import pygame.locals
from player import Player
import time
from boomer_client import BoomerClient

explosions = []


def setup_player(player_id):
    if player_id == 0:
        return Player(0, 0, 0, 100)
    elif player_id == 1:
        return Player(526, 0, 1, 100)
    elif player_id == 2:
        return Player(0, 526, 2, 100)
    elif player_id == 3:
        return Player(526, 526, 3, 100)


def display_hp(player, hp):
    text_rect = hp.get_rect()
    if player == 0:
        text_rect.topleft = (68, 76)
    elif player == 1:
        text_rect.topleft = (452, 76)
    elif player == 2:
        text_rect.topleft = (68, 460)
    elif player == 3:
        text_rect.topleft = (452, 460)
    return text_rect


def draw_window(screen, players, walls, bombs):
    wall_points = [86, 214, 342, 470]
    screen.fill((0, 0, 0))
    font = pg.font.Font("freesansbold.ttf", 32)
    for wall in walls:
        pg.draw.rect(screen, (255, 255, 255), wall)
    for player in players:
        if players[player].hp > 0:
            pg.draw.rect(screen, players[player].color,
                         players[player].rect)
        hp = font.render(str(players[player].hp), True, players[player].color)
        screen.blit(hp, display_hp(player, hp))
        if player in bombs:
            if bombs[player] is not None:
                pg.draw.rect(screen, (255, 255, 0), (bombs[player]['position'][0],
                                                     bombs[player]['position'][1], 20, 20))
    for explosion in explosions:
        # (explosion)
        # print(time.time() - explosion['countdown'])
        if time.time() - explosion['countdown'] < 2:
            # print("here")
            if explosion['x'] not in wall_points:
                # print(explosion['x'])
                pg.draw.rect(screen, (255, 101, 0), (explosion['x']-6, explosion['y']-118, 30, 256))
            if explosion['y'] not in wall_points:
                pg.draw.rect(screen, (255, 101, 0), (explosion['x']-118, explosion['y']-6, 256, 30))
        else:
            del explosions[explosions.index(explosion)]
    pg.display.update()


def main():
    # host = input("Host(IPv4 or name): ")
    host = "127.0.0.1"
    player_name = input("Player name: ")

    client = BoomerClient()
    client.connect_in_thread(hostname=host, port=28960)
    client.dispatch_event("JOIN", player_name)
    while client.player_id is None:
        pass

    clock = pg.time.Clock()
    pg.init()
    screen_width = 576
    screen_height = 576
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Ok Boomer!")
    my_player = setup_player(client.player_id)
    game_on = True
    players = {client.player_id: my_player}
    bombs = {}

    walls = [pg.Rect(64, 64, 64, 64), pg.Rect(192, 64, 64, 64),
             pg.Rect(320, 64, 64, 64), pg.Rect(448, 64, 64, 64),
             pg.Rect(64, 192, 64, 64), pg.Rect(64, 320, 64, 64),
             pg.Rect(64, 448, 64, 64), pg.Rect(192, 448, 64, 64),
             pg.Rect(320, 448, 64, 64), pg.Rect(448, 448, 64, 64),
             pg.Rect(448, 192, 64, 64), pg.Rect(448, 320, 64, 64),
             pg.Rect(320, 320, 64, 64), pg.Rect(192, 192, 64, 64),
             pg.Rect(320, 192, 64, 64), pg.Rect(192, 320, 64, 64)]

    while game_on:
        dt = clock.tick(60)
        draw_window(screen, players, walls, bombs)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_on = False
        my_player.move(client, walls)
        with client.access_game_state() as game_state:
            client.dispatch_event(
                event_type="MOVE",
                player_id=client.player_id,
                new_position=(my_player.rect.x, my_player.rect.y),
            )

            for player_id, player in game_state.players.items():
                x, y = [int(c) for c in player['position']]
                hp = player['hp']
                # print(game_state.players)
                if player_id in players:
                    players[player_id].rect.x, players[player_id].rect.y = x, y
                    players[player_id].hp = hp
                else:
                    players[player_id] = Player(x, y, player_id, hp)

            for player_id, bomb in game_state.bombs.items():
                if bomb is not None:
                    bombs[player_id] = bomb
                else:
                    bombs[player_id] = None

            for player_id, explosion in game_state.explosions.items():
                if explosion is not None:
                    if explosion['id'] not in explosions:
                        explosions.append({'id': explosion['id'],
                                           'x': explosion['position'][0],
                                           'y': explosion['position'][1],
                                           'countdown': time.time()})


    pg.quit()
    client.disconnect(shutdown_server=False)


if __name__ == "__main__":
    main()

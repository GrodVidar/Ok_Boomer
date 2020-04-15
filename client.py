from pygase import Client
import pygame as pg
import pygame.locals
from time import sleep
from player import Player
from boomer_client import BoomerClient


def setup_player(player_id):
    if player_id == 0:
        return Player(0, 0, (50, 255, 50))
    elif player_id == 1:
        return Player(526, 0, (255, 50, 50))
    elif player_id == 2:
        return Player(0, 526, (50, 50, 255))
    elif player_id == 3:
        return Player(526, 526, (255, 255, 255))


def draw_window(screen, players, walls):
    screen.fill((0, 0, 0))
    for i in walls:
        pg.draw.rect(screen, (255, 255, 255), i)
    for i in players:
        pg.draw.rect(screen, players[i].color,
                     players[i].rect)
    pg.display.update()


def main():
    # host = input("Host(IPv4 or name): ")
    host = "127.0.0.1"
    player_name = input("Player name: ")

    client = BoomerClient()
    client.connect_in_thread(hostname=host, port=1337)
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
        draw_window(screen, players, walls)
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
                if player_id == 0 and client.player_id != 0:
                    players[player_id] = Player(x, y, (50, 255, 50))
                elif player_id == 1 and client.player_id != 1:
                    players[player_id] = Player(x, y, (255, 50, 50))
                elif player_id == 2 and client.player_id != 2:
                    players[player_id] = Player(x, y, (50, 50, 255))
                elif player_id == 3 and client.player_id != 3:
                    players[player_id] = Player(x, y, (255, 255, 255))
                if player_id == client.player_id:
                    my_player.rect.x, my_player.rect.y = [int(c) for c in player['position']]
                # print(f"x: {x} y: {y}")
    pg.quit()
    client.disconnect(shutdown_server=True)


if __name__ == "__main__":
    main()

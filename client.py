from pygase import Client
import pygame as pg
import pygame.locals
from time import sleep
from player import Player
from boomer_client import BoomerClient


def setup_player(player_id):
    if player_id == 0:
        return Player(0, 0, 64, 64, (50, 255, 50))
    elif player_id == 1:
        return Player(570, 0, 64, 64, (255, 50, 50))
    elif player_id == 2:
        return Player(0, 570, 64, 64, (50, 50, 255))
    elif player_id == 3:
        return Player(570, 570, 64, 64, (255, 255, 255))


def draw_window(screen, players):
    screen.fill((0, 0, 0))
    for i in players:
        pg.draw.rect(screen, i.color, (i.x, i.y, i.width, i.height))
    pg.display.update()


def main():
    #host = input("Host(IPv4 or name): ")
    host = "127.0.0.1"
    player_name = input("Player name: ")

    client = BoomerClient()
    client.connect_in_thread(hostname=host, port=1337)
    client.dispatch_event("JOIN", player_name)
    while client.player_id is None:
        pass

    clock = pg.time.Clock()
    pg.init()
    screen_width = 640
    screen_height = 640
    screen = pg.display.set_mode((screen_width, screen_height))
    my_player = setup_player(client.player_id)
    game_on = True
    players = set()
    players.add(my_player)
    while game_on:
        dt = clock.tick(60)
        draw_window(screen, players)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_on = False
        my_player.move()
        with client.access_game_state() as game_state:
            old_pos = game_state.players[client.player_id]['position']
            client.dispatch_event(
                event_type="MOVE",
                player_id=client.player_id,
                new_position=(my_player.x, my_player.y),
            )

            for player_id, player in game_state.players.items():
                x, y = [int(c) for c in player['position']]
                if player_id == 0 and client.player_id != 0:
                    players.add(Player(x, y, 64, 64, (50, 255, 50)))
                elif player_id == 1 and client.player_id != 1:
                    players.add(Player(x, y, 64, 64, (255, 50, 50)))
                elif player_id == 2 and client.player_id != 2:
                    players.add(Player(x, y, 64, 64, (50, 50, 255)))
                elif player_id == 3 and client.player_id != 3:
                    players.add(Player(x, y, 64, 64, (255, 255, 255)))
                if player_id == client.player_id:
                    my_player.x, my_player.y = [int(c) for c in player['position']]
                #print(f"x: {x} y: {y}")
    pg.quit()
    client.disconnect(shutdown_server=True)


if __name__ == "__main__":
    main()

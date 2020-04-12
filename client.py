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
        return Player(570, 0, (255, 50, 50))
    elif player_id == 2:
        return Player(0, 570, (50, 50, 255))
    elif player_id == 3:
        return Player(570, 570, (255, 255, 255))


def draw_window(screen, players, all_sprites):
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    for i in players:
        pg.draw.rect(screen, players[i].color,
                     (players[i].x, players[i].y, players[i].width, players[i].height))
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
    screen_width = 640
    screen_height = 640
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Ok Boomer!")
    my_player = setup_player(client.player_id)
    game_on = True
    players = {client.player_id: my_player}

    all_sprites = pg.sprite.Group()
    while game_on:
        dt = clock.tick(60)
        all_sprites.update()
        draw_window(screen, players, all_sprites)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_on = False
        my_player.move(client)
        with client.access_game_state() as game_state:
            client.dispatch_event(
                event_type="MOVE",
                player_id=client.player_id,
                new_position=(my_player.x, my_player.y),
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
                    my_player.x, my_player.y = [int(c) for c in player['position']]
                # print(f"x: {x} y: {y}")
    pg.quit()
    client.disconnect(shutdown_server=True)


if __name__ == "__main__":
    main()

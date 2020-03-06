from pygase import Client
import pygame as pg
import pygame.locals


class BoomerClient(Client):
    def __init__(self):
        super().__init__()
        self.player_id = None
        self.register_event_handler("PLAYER_CREATED", self.on_player_created)

    def on_player_created(self, player_id):
        self.player_id = player_id


client = BoomerClient()

if __name__ == "__main__":
    host = input("Host(IPv4 or name): ")
    player_name = input("Player name: ")
    client.connect_in_thread(hostname=host, port=1337)
    client.dispatch_event("JOIN", player_name)
    while client.player_id is None:
        pass

    keys_pressed = set()
    clock = pg.time.Clock()

    pg.init()
    screen_width = 640
    screen_height = 640
    screen = pg.display.set_mode((screen_width, screen_height))
    movement_speed = 10

    game_on = True
    while game_on:
        dt = clock.tick(60)
        screen.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == pg.locals.QUIT:
                game_on = False
            if event.type == pg.locals.KEYDOWN:
                keys_pressed.add(event.key)
            if event.type == pg.locals.KEYUP:
                keys_pressed.remove(event.key)

        dx, dy = 0, 0
        if pg.locals.K_DOWN in keys_pressed:
            dy += movement_speed
        elif pg.locals.K_UP in keys_pressed:
            dy -= movement_speed
        elif pg.locals.K_RIGHT in keys_pressed:
            dx += movement_speed
        elif pg.locals.K_LEFT in keys_pressed:
            dx -= movement_speed

        if pg.locals.K_SPACE in keys_pressed:
            # Place Bomb
            pass

        with client.access_game_state() as game_state:
            old_pos = game_state.players[client.player_id]['position']
            client.dispatch_event(
                event_type="MOVE",
                player_id=client.player_id,
                new_position=((old_pos[0] + dx), (old_pos[1] + dy)),
            )

            for player_id, player in game_state.players.items():
                if player_id == 0:
                    color = (50, 255, 50)
                elif player_id == 1:
                    color = (255, 50, 50)
                elif player_id == 2:
                    color = (50, 50, 255)
                elif player_id == 3:
                    color = (255, 255, 255)

                x, y = [int(coordinate) for coordinate in player['position']]
                # print(f"x: {x} y: {y}")
                pg.draw.rect(screen, color, (x, y, 64, 64))
        pg.display.flip()

    pg.quit()

    client.disconnect(shutdown_server=True)

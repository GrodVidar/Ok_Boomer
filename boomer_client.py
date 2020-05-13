from pygase import Client


# this class is what acts as the bridge of the functions called from the server and from the game.
class BoomerClient(Client):
    def __init__(self):
        super().__init__()
        self.player_id = None
        self.register_event_handler("PLAYER_CREATED", self.on_player_created)

    def on_player_created(self, player_id):
        self.player_id = player_id

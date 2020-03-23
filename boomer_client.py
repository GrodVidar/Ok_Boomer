from pygase import Client


class BoomerClient(Client):
    def __init__(self):
        super().__init__()
        self.player_id = None
        self.register_event_handler("PLAYER_CREATED", self.on_player_created)

    def on_player_created(self, player_id):
        self.player_id = player_id

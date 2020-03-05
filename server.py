import math
from pygase import GameState, Backend


initial_game_state = GameState(players={}, bombs={})


def time_step(game_state, dt):
    # Make the imaginary enemy move in sinuous lines like a drunkard.
    if len(game_state.players) < 2:
        return{}


def on_move(player_id, new_position, **kwargs):
    return {"players": {player_id: {"position": new_position}}}


backend = Backend(initial_game_state, time_step, event_handlers={'MOVE': on_move})


def on_bomb(player_id, **kwargs):
    pass


backend.game_state_machine.register_event_handler("BOMB", on_bomb)


def on_join(player_name, game_state, client_address, **kwargs):
    print(f"{player_name} has joined.")
    player_id = len(game_state.players)

    backend.server.dispatch_event("PLAYER_CREATED", player_id, target_client=client_address)
    if player_id == 0:
        return{
            "players": {player_id: {"name": player_name, "position": (0, 10), "hp": 100}}
        }
    if player_id == 1:
        return{
            "players": {player_id: {"name": player_name, "position": (10, 10), "hp": 100}}
        }
    if player_id == 2:
        return{
            "players": {player_id: {"name": player_name, "position": (0, 0), "hp": 100}}
        }
    if player_id == 3:
        return{
            "players": {player_id: {"name": player_name, "position": (10, 0), "hp": 100}}
        }


backend.game_state_machine.register_event_handler("JOIN", on_join)

if __name__ == "__main__":
    backend.run('', port=1337)

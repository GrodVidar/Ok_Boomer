from pygase import GameState, Backend


def time_step(game_state, dt):
    if len(game_state.players) < 5:
        return{}


def on_move(player_id, new_position, **kwargs):
    return {"players": {player_id: {"position": new_position}}}


def on_bomb(player_id, position, **kwargs):
    print(f"bomb placed by: {player_id} at {position}")

    return {"bombs": {player_id: {"position": position}}}


def on_join(player_name, game_state, client_address, **kwargs):
    print(f"{player_name} has joined.")
    player_id = len(game_state.players)

    backend.server.dispatch_event("PLAYER_CREATED", player_id, target_client=client_address)
    if player_id == 0:
        return{
            "players": {player_id: {"name": player_name, "position": (0, 0), "hp": 100,
                                    "power_ups": {"faster": False, "more_bombs": False}}}
        }
    if player_id == 1:
        return{
            "players": {player_id: {"name": player_name, "position": (570, 0), "hp": 100,
                                    "power_ups": {"faster": False, "more_bombs": False}}}
        }
    if player_id == 2:
        return{
            "players": {player_id: {"name": player_name, "position": (0, 570), "hp": 100,
                                    "power_ups": {"faster": False, "more_bombs": False}}}
        }
    if player_id == 3:
        return{
            "players": {player_id: {"name": player_name, "position": (570, 570), "hp": 100,
                                    "power_ups": {"faster": False, "more_bombs": False}}}
        }


if __name__ == "__main__":
    initial_game_state = GameState(players={}, bombs={})
    backend = Backend(initial_game_state, time_step, event_handlers={'MOVE': on_move})
    backend.game_state_machine.register_event_handler("BOMB", on_bomb)
    backend.game_state_machine.register_event_handler("JOIN", on_join)
    backend.run('', port=1337)

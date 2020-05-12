from pygase import GameState, Backend
import time
from random import randint

bombs = []
wall_points = [86, 214, 342, 470]


def damage_player(players):
    info = []
    for player in players:
        print("BAM")
        players[player]['hp'] -= 10
        print(players[player]['hp'])
        players[player]['damaged'] = time.time()
        info.append({player: {'hp': players[player]['hp'], 'damaged': players[player]['damaged']}})
        # info[player] = {'players': {player: {"hp": stats['hp'], 'damaged': stats['damaged']}}}
    return info


def time_step(game_state, dt):
    if len(game_state.players) < 1:
        return{}
    else:
        for player_id, bomb in game_state.bombs.items():
            if bomb is not None:
                if not bomb['exploded']:
                    bomb['countdown'] -= dt
                    if bomb['countdown'] <= 0:
                        bomb['exploded'] = True
                        return {'bombs': {player_id: None},
                                'explosions': {player_id: {'id': randint(1, 50),
                                                           'position': bomb['position'], 'countdown': 2.0}}}
        players_damaged = {}
        for pid, explosion in game_state.explosions.items():
            if explosion is not None:
                if explosion['countdown'] > 0:
                    explosion['countdown'] -= dt
                    vertical_ex = False
                    horizontal_ex = False
                    ex_x = explosion['position'][0]
                    ex_y = explosion['position'][1]
                    if ex_x not in wall_points:
                        vertical_ex = True
                    if ex_y not in wall_points:
                        horizontal_ex = True
                    for player_id, stats in game_state.players.items():
                        player_pos = stats['position']
                        if vertical_ex:
                            vertical_hit = False
                            horizontal_hit = False
                            if ex_x < player_pos[0] + 50 < ex_x + 30 or ex_x < player_pos[0] < ex_x + 30 or player_pos[0] < ex_x < player_pos[0] + 50:
                                horizontal_hit = True
                            if ex_y - 128 < player_pos[1] + 50 < ex_y + 128 or ex_y - 128 < player_pos[1] < ex_y + 128:
                                vertical_hit = True
                            if horizontal_hit and vertical_hit and time.time() - stats['damaged'] > 3:
                                players_damaged[player_id] = stats
                                # return damage_player(stats, player_id)
                        if horizontal_ex:
                            vertical_hit = False
                            horizontal_hit = False
                            if ex_y < player_pos[1] + 50 < ex_y + 30 or ex_y < player_pos[1] < ex_y + 30 or player_pos[1] < ex_y < player_pos[1] + 50:
                                vertical_hit = True
                            if ex_x - 128 < player_pos[0] + 50 < ex_x + 128 or ex_x - 128 < player_pos[0] < ex_x + 128:
                                horizontal_hit = True
                            if horizontal_hit and vertical_hit and time.time() - stats['damaged'] > 3:
                                players_damaged[player_id] = stats
                                # return damage_player(stats, player_id)
                else:
                    return {'explosions': {player_id: None}}
        info = damage_player(players_damaged)
        # print(game_state.players)
        return {'players': x for x in info}
    return {}


def on_move(player_id, new_position, **kwargs):
    return {"players": {player_id: {"position": new_position}}}


def on_bomb(player_id, position, **kwargs):
    print(f"bomb placed by: {player_id} at {position}")
    return {"bombs": {player_id: {"position": position, "countdown": 3.0, "exploded": False}}}


def on_join(player_name, game_state, client_address, **kwargs):
    print(f"{player_name} has joined.")
    player_id = len(game_state.players)

    backend.server.dispatch_event("PLAYER_CREATED", player_id, target_client=client_address)
    if player_id == 0:
        return{
            "players": {player_id: {"name": player_name, "position": (0, 0), "hp": 100, 'damaged': 0}}
        }
    if player_id == 1:
        return{
            "players": {player_id: {"name": player_name, "position": (526, 0), "hp": 100, 'damaged': 0}}
        }
    if player_id == 2:
        return{
            "players": {player_id: {"name": player_name, "position": (0, 526), "hp": 100, 'damaged': 0}}
        }
    if player_id == 3:
        return{
            "players": {player_id: {"name": player_name, "position": (526, 526), "hp": 100, 'damaged': 0}}
        }


if __name__ == "__main__":
    initial_game_state = GameState(players={}, bombs={}, explosions={})
    backend = Backend(initial_game_state, time_step, event_handlers={'MOVE': on_move})
    backend.game_state_machine.register_event_handler("BOMB", on_bomb)
    backend.game_state_machine.register_event_handler("JOIN", on_join)
    try:
        backend.run('', port=28960)
    except ConnectionResetError:
        pass

import threading
from flask import request
from flask_socketio import emit, join_room

from game_rooms import room_manager, Player


def register_socket_events(socketio):

    @socketio.on("connect")
    def on_connect():
        print(f"Client connected: {request.sid}")

    @socketio.on("disconnect")
    def on_disconnect():
        print(f"Client disconnected: {request.sid}")

        room = room_manager.remove_player(request.sid)

        if room:
            for player in room.players:
                emit("opponent_disconnect", {}, to=player.sid)

    @socketio.on("join_queue")
    def on_join_queue(data):
        name = data.get("name", "").strip()

        if not name:
            emit("error", {"message": "Name is required"})
            return

        if len(name) > 20:
            name = name[:20]

        player = Player(sid=request.sid, name=name)
        match = room_manager.add_to_queue(player)

        if match:
            player1, player2 = match
            room = room_manager.create_room(player1, player2)

            join_room(room.room_id, sid=player1.sid)
            join_room(room.room_id, sid=player2.sid)

            emit("match_found", {
                "room_id": room.room_id,
                "opponent_name": player2.name
            }, to=player1.sid)

            emit("match_found", {
                "room_id": room.room_id,
                "opponent_name": player1.name
            }, to=player2.sid)

            start_countdown(socketio, room)
        else:
            emit("queue_status", {"status": "waiting"})

    @socketio.on("player_pos")
    def on_player_pos(data):
        room = room_manager.get_player_room(request.sid)

        if not room or room.state != "racing":
            return

        x = data.get("x", 0)
        y = data.get("y", 0)

        for player in room.players:
            if player.sid == request.sid:
                player.position = (x, y)
                break

        opponent = room.get_opponent(request.sid)
        if opponent:
            emit("opponent_pos", {"x": x, "y": y}, to=opponent.sid)

    @socketio.on("player_finish")
    def on_player_finish(data):
        room = room_manager.get_player_room(request.sid)

        if not room or room.state != "racing":
            return

        time_ms = data.get("time_ms")
        if time_ms is None:
            return

        try:
            time_ms = int(time_ms)
        except (ValueError, TypeError):
            return

        player_name = None
        for player in room.players:
            if player.sid == request.sid:
                player_name = player.name
                break

        if not player_name:
            return

        room.record_finish(player_name, time_ms)

        if room.all_finished():
            room_manager.finish_room(room.room_id)

            winner = room.get_winner()

            emit("race_result", {
                "winner": winner,
                "times": room.finish_times
            }, to=room.room_id)


def start_countdown(socketio, room):
    def countdown_thread():
        room.state = "countdown"

        for count in [3, 2, 1]:
            socketio.emit("countdown", {"count": count}, to=room.room_id)
            socketio.sleep(1)

        room_manager.start_race(room.room_id)
        socketio.emit("race_start", {}, to=room.room_id)

    thread = threading.Thread(target=countdown_thread)
    thread.daemon = True
    thread.start()

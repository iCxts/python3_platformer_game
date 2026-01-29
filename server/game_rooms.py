import uuid
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Player:
    sid: str
    name: str
    position: tuple = (0, 0)


@dataclass
class GameRoom:
    room_id: str
    players: list = field(default_factory=list)
    state: str = "waiting"
    start_time: float = 0.0
    finish_times: dict = field(default_factory=dict)

    def get_opponent(self, sid: str) -> Optional[Player]:
        for player in self.players:
            if player.sid != sid:
                return player
        return None

    def add_player(self, player: Player) -> bool:
        if len(self.players) >= 2:
            return False
        self.players.append(player)
        return True

    def is_full(self) -> bool:
        return len(self.players) >= 2

    def record_finish(self, player_name: str, time_ms: int):
        self.finish_times[player_name] = time_ms

    def all_finished(self) -> bool:
        return len(self.finish_times) >= len(self.players)

    def get_winner(self) -> Optional[str]:
        if not self.all_finished():
            return None
        return min(self.finish_times, key=self.finish_times.get)


class RoomManager:
    def __init__(self):
        self.queue: list[Player] = []
        self.rooms: dict[str, GameRoom] = {}
        self.player_rooms: dict[str, str] = {}

    def add_to_queue(self, player: Player) -> Optional[tuple[Player, Player]]:
        for p in self.queue:
            if p.sid == player.sid:
                return None

        self.queue.append(player)
        return self.try_match()

    def try_match(self) -> Optional[tuple[Player, Player]]:
        if len(self.queue) >= 2:
            player1 = self.queue.pop(0)
            player2 = self.queue.pop(0)
            return (player1, player2)
        return None

    def create_room(self, player1: Player, player2: Player) -> GameRoom:
        room_id = str(uuid.uuid4())[:8]
        room = GameRoom(room_id=room_id)
        room.add_player(player1)
        room.add_player(player2)

        self.rooms[room_id] = room
        self.player_rooms[player1.sid] = room_id
        self.player_rooms[player2.sid] = room_id

        return room

    def get_room(self, room_id: str) -> Optional[GameRoom]:
        return self.rooms.get(room_id)

    def get_player_room(self, sid: str) -> Optional[GameRoom]:
        room_id = self.player_rooms.get(sid)
        if room_id:
            return self.rooms.get(room_id)
        return None

    def remove_player(self, sid: str) -> Optional[GameRoom]:
        self.queue = [p for p in self.queue if p.sid != sid]

        room_id = self.player_rooms.pop(sid, None)
        if room_id and room_id in self.rooms:
            room = self.rooms[room_id]
            room.players = [p for p in room.players if p.sid != sid]

            if len(room.players) == 0:
                del self.rooms[room_id]
                return None

            return room
        return None

    def start_race(self, room_id: str):
        room = self.rooms.get(room_id)
        if room:
            room.state = "racing"
            room.start_time = time.time()

    def finish_room(self, room_id: str):
        room = self.rooms.get(room_id)
        if room:
            room.state = "finished"


room_manager = RoomManager()

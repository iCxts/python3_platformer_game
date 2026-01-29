import socketio
from config import SERVER_URL


class Network:
    def __init__(self):
        self.sio = socketio.Client()
        self.connected = False
        self.in_queue = False
        self.matched = False
        self.room_id = None
        self.opponent_name = ""
        self.opponent_pos = (0, 0)
        self.countdown = 0
        self.race_started = False
        self.race_result = None
        self.opponent_disconnected = False

        self._register_events()

    def _register_events(self):
        @self.sio.on("connect")
        def on_connect():
            self.connected = True

        @self.sio.on("disconnect")
        def on_disconnect():
            self.connected = False
            self.matched = False
            self.race_started = False

        @self.sio.on("queue_status")
        def on_queue_status(data):
            if data.get("status") == "waiting":
                self.in_queue = True

        @self.sio.on("match_found")
        def on_match_found(data):
            self.matched = True
            self.in_queue = False
            self.room_id = data.get("room_id")
            self.opponent_name = data.get("opponent_name", "Opponent")

        @self.sio.on("countdown")
        def on_countdown(data):
            self.countdown = data.get("count", 0)

        @self.sio.on("race_start")
        def on_race_start():
            self.race_started = True
            self.countdown = 0

        @self.sio.on("opponent_pos")
        def on_opponent_pos(data):
            self.opponent_pos = (data.get("x", 0), data.get("y", 0))

        @self.sio.on("race_result")
        def on_race_result(data):
            self.race_result = data

        @self.sio.on("opponent_disconnect")
        def on_opponent_disconnect():
            self.opponent_disconnected = True

    def connect(self):
        if not self.connected:
            try:
                self.sio.connect(SERVER_URL)
                return True
            except Exception:
                return False
        return True

    def disconnect(self):
        if self.connected:
            self.sio.disconnect()
        self.reset()

    def join_queue(self, name):
        if self.connected:
            self.sio.emit("join_queue", {"name": name})

    def send_position(self, x, y):
        if self.connected and self.race_started:
            self.sio.emit("player_pos", {"x": x, "y": y})

    def send_finish(self, time_ms):
        if self.connected:
            self.sio.emit("player_finish", {"time_ms": time_ms})

    def reset(self):
        self.in_queue = False
        self.matched = False
        self.room_id = None
        self.opponent_name = ""
        self.opponent_pos = (0, 0)
        self.countdown = 0
        self.race_started = False
        self.race_result = None
        self.opponent_disconnected = False

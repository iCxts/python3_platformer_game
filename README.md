# Platformer Speedrun Game

A platformer speedrunning game with solo and multiplayer modes.

## Setup

```bash
pip install -r requirements.txt
```

## Run

**Start server:**
```bash
cd server && python app.py
```

**Start game:**
```bash
cd game && python main.py
```

## Controls

| Key | Action |
|-----|--------|
| A/D or Arrow Keys | Move |
| W/Space/Up | Jump |
| ESC | Back to menu |

## Multiplayer (LAN)

1. Start server on one PC
2. On other PCs, edit `game/config.py`:
   ```python
   SERVER_URL = "http://<server-ip>:3000"
   ```
3. Both players click "Multiplayer" and wait for match

## Project Structure

```
├── game/
│   ├── main.py
│   ├── config.py
│   ├── player.py
│   ├── level.py
│   ├── timer.py
│   ├── menu.py
│   ├── network.py
│   ├── opponent.py
│   ├── assets/
│   └── levels/
│
├── server/
│   ├── app.py
│   ├── routes.py
│   ├── socket_events.py
│   ├── game_rooms.py
│   └── models.py
│
└── webapp/
    ├── templates/
    └── static/
```

## Leaderboard

View at `http://localhost:3000/leaderboard`

Reset:
```bash
rm server/database.db
```

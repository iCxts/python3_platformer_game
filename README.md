# Platformer Speedrun Game - Project Structure

## Overview
A platformer speedrunning game with solo and multiplayer modes. Players race to the finish line with the least time possible. Features a web-based leaderboard and real-time multiplayer via WebSockets.

---

## Directory Structure

```
python3_platformer_game/
│
├── game/                       
│   ├── __init__.py
│   ├── main.py                  
│   ├── config.py                 
│   ├── player.py                 
│   ├── opponent.py                
│   ├── level.py                  
│   ├── camera.py                 
│   ├── timer.py                   
│   ├── network.py                 
│   ├── menu.py                    
│   ├── leaderboard_view.py         
│   │
│   ├── assets/
│   │   ├── sprites/
│   │   │   ├── player.png          
│   │   │   └── opponent.png       
│   │   │
│   │   ├── tiles/
│   │   │   ├── ground.png        
│   │   │   ├── platform.png     
│   │   │   ├── finish.png       
│   │   │   └── start.png          
│   │   │
│   │   ├── backgrounds/
│   │   │   └── background.png      
│   │   │
│   │   └── ui/
│   │       ├── button.png        
│   │       └── timer_bg.png       
│   │
│   └── levels/
│       └── level1.json           
│
├── server/                       
│   ├── __init__.py
│   ├── app.py                   
│   ├── config.py                   
│   ├── models.py                   
│   ├── database.py                 
│   ├── routes.py                   
│   ├── socket_events.py           
│   ├── game_rooms.py               
│   └── database.db                
│
├── webapp/                        
│   ├── templates/
│   │   ├── base.html              
│   │   ├── leaderboard.html      
│   │   └── index.html              
│   │
│   └── static/
│       ├── css/
│       │   └── style.css           
│       └── js/
│           └── leaderboard.js     
│
└── requirements.txt              
```

---

## Module Descriptions

### Game Client (`game/`)

| File | Purpose |
|------|---------|
| `main.py` | Initializes Pygame, runs game loop, handles state transitions |
| `config.py` | Screen dimensions, colors, physics constants, server URL |
| `player.py` | Player sprite, input handling, gravity, jumping, collision response |
| `opponent.py` | Renders opponent position received from server as ghost |
| `level.py` | Loads JSON level, creates tile sprites, handles collision detection |
| `camera.py` | Viewport that follows player, handles level boundaries |
| `timer.py` | Tracks elapsed time, starts on first input, formats display |
| `network.py` | Socket.IO client, emits position, receives opponent data |
| `menu.py` | Main menu, name input screen, mode selection |
| `leaderboard_view.py` | Fetches and displays leaderboard within the game |

### Server (`server/`)

| File | Purpose |
|------|---------|
| `app.py` | Creates Flask app, initializes SocketIO, registers blueprints |
| `config.py` | Database URI, secret key, CORS settings |
| `models.py` | SQLAlchemy model for leaderboard entries |
| `database.py` | Database session management, initialization |
| `routes.py` | REST endpoints: GET/POST `/api/leaderboard` |
| `socket_events.py` | Handles: `join_queue`, `player_pos`, `player_finish`, `disconnect` |
| `game_rooms.py` | Room creation, player pairing, state management |

### Webapp (`webapp/`)

| File | Purpose |
|------|---------|
| `templates/base.html` | Common HTML structure, navbar |
| `templates/leaderboard.html` | Displays top times in a table |
| `templates/index.html` | Landing page with game info |
| `static/css/style.css` | Styling for web pages |

---

## Data Models

### Leaderboard Entry
```python
class LeaderboardEntry:
    id: int                 # Primary key
    player_name: str        # Player's name (max 20 chars)
    time_ms: int            # Completion time in milliseconds
    created_at: datetime    # When the record was set
```

### Game Room (In-Memory)
```python
class GameRoom:
    room_id: str            # Unique room identifier
    players: list           # [{"sid": str, "name": str, "position": tuple}, ...]
    state: str              # "waiting" | "countdown" | "racing" | "finished"
    start_time: float       # Timestamp when race started
    finish_times: dict      # {"player_name": time_ms, ...}
```

---

## API Endpoints

### REST API

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/api/leaderboard` | Get top 10 scores | - | `[{name, time_ms, created_at}, ...]` |
| POST | `/api/leaderboard` | Submit new score | `{name, time_ms}` | `{success, rank}` |
| GET | `/` | Web leaderboard page | - | HTML |

### WebSocket Events

| Event | Direction | Payload | Description |
|-------|-----------|---------|-------------|
| `join_queue` | Client → Server | `{name: str}` | Join multiplayer matchmaking |
| `queue_status` | Server → Client | `{status: str}` | "waiting" or "matched" |
| `match_found` | Server → Client | `{room_id, opponent_name}` | Opponent found |
| `countdown` | Server → Client | `{count: int}` | 3, 2, 1 countdown |
| `race_start` | Server → Client | `{}` | Race begins |
| `player_pos` | Client → Server | `{x, y}` | Send current position |
| `opponent_pos` | Server → Client | `{x, y}` | Receive opponent position |
| `player_finish` | Client → Server | `{time_ms: int}` | Player reached finish |
| `race_result` | Server → Client | `{winner, times}` | Final results |
| `opponent_disconnect` | Server → Client | `{}` | Opponent left |

---

## Game States

```
┌─────────────┐
│    MENU     │ ◄─────────────────────────────┐
└──────┬──────┘                               │
       │                                      │
       ▼                                      │
┌─────────────┐     ┌─────────────┐          │
│ NAME_INPUT  │────►│   WAITING   │ (multiplayer only)
└──────┬──────┘     └──────┬──────┘          │
       │                   │                  │
       │ (solo)            │ (matched)        │
       ▼                   ▼                  │
┌─────────────┐     ┌─────────────┐          │
│  COUNTDOWN  │◄────│  COUNTDOWN  │          │
└──────┬──────┘     └──────┬──────┘          │
       │                   │                  │
       ▼                   ▼                  │
┌─────────────┐     ┌─────────────┐          │
│   PLAYING   │     │   PLAYING   │          │
│   (solo)    │     │ (multiplayer)│          │
└──────┬──────┘     └──────┬──────┘          │
       │                   │                  │
       ▼                   ▼                  │
┌─────────────┐     ┌─────────────┐          │
│   RESULT    │─────│   RESULT    │──────────┘
│ (show time) │     │(show winner)│
└─────────────┘     └─────────────┘
```

---

## Running the Application

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
cd server
python app.py
```
Server runs on `http://localhost:5000`

### 3. Start Game Client(s)
```bash
cd game
python main.py
```

For multiplayer: Run two instances of the game client.

### 4. View Web Leaderboard
Open browser to `http://localhost:5000`


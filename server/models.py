from datetime import datetime
from database import db


class LeaderboardEntry(db.Model):
    __tablename__ = "leaderboard_entry"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_name = db.Column(db.String(20), nullable=False)
    time_ms = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "player_name": self.player_name,
            "time_ms": self.time_ms,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

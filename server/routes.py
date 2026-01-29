from flask import Blueprint, request, jsonify
from database import db
from models import LeaderboardEntry

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    entries = (
        LeaderboardEntry.query
        .order_by(LeaderboardEntry.time_ms.asc())
        .limit(10)
        .all()
    )
    return jsonify([entry.to_dict() for entry in entries])


@api.route("/leaderboard", methods=["POST"])
def submit_score():
    data = request.get_json()
    name = data.get("name", "Player")
    time_ms = int(data.get("time_ms", 0))

    entry = LeaderboardEntry(player_name=name, time_ms=time_ms)
    db.session.add(entry)
    db.session.commit()

    rank = LeaderboardEntry.query.filter(LeaderboardEntry.time_ms < time_ms).count() + 1
    return jsonify({"success": True, "rank": rank})

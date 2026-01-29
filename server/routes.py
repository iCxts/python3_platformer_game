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
    return jsonify([entry.to_dict() for entry in entries]), 200


@api.route("/leaderboard", methods=["POST"])
def submit_score():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body required"}), 400

    name = data.get("name", "").strip()
    time_ms = data.get("time_ms")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    if len(name) > 20:
        return jsonify({"error": "Name must be 20 characters or less"}), 400

    if time_ms is None:
        return jsonify({"error": "time_ms is required"}), 400

    try:
        time_ms = int(time_ms)
        if time_ms <= 0:
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({"error": "time_ms must be a positive integer"}), 400

    entry = LeaderboardEntry(player_name=name, time_ms=time_ms)
    db.session.add(entry)
    db.session.commit()

    rank = (
        LeaderboardEntry.query
        .filter(LeaderboardEntry.time_ms < time_ms)
        .count()
    ) + 1

    return jsonify({"success": True, "rank": rank}), 201

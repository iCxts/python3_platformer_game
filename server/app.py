from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS

import config
from database import init_db
from routes import api
from socket_events import register_socket_events


def create_app():
    app = Flask(
        __name__,
        template_folder="../webapp/templates",
        static_folder="../webapp/static"
    )

    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS

    CORS(app, origins=config.CORS_ORIGINS)

    init_db(app)

    app.register_blueprint(api)

    socketio = SocketIO(
        app,
        cors_allowed_origins=config.CORS_ORIGINS,
        async_mode="threading"
    )

    register_socket_events(socketio)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/leaderboard")
    def leaderboard_page():
        from models import LeaderboardEntry

        entries = (
            LeaderboardEntry.query
            .order_by(LeaderboardEntry.time_ms.asc())
            .limit(10)
            .all()
        )
        return render_template("leaderboard.html", entries=entries)

    return app, socketio


app, socketio = create_app()


if __name__ == "__main__":
    print(f"Starting server on http://{config.HOST}:{config.PORT}")
    socketio.run(app, host=config.HOST, port=config.PORT, debug=config.DEBUG)

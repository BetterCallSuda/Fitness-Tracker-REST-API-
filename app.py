from flask import Flask, request, jsonify
from models import db, User, Workout


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fitness.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# -----------------------------
# CREATE USER
# -----------------------------
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    user = User(
        name=data["name"],
        email=data["email"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201



# -----------------------------
# GET ALL USERS
# -----------------------------
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

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



# -----------------------------
# ADD WORKOUT
# -----------------------------
@app.route("/workouts", methods=["POST"])
def add_workout():
    data = request.get_json()

    user = User.query.get(data["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    workout = Workout(
        workout_type=data["workout_type"],
        duration_minutes=data["duration_minutes"],
        user=user
    )

    db.session.add(workout)
    db.session.commit()

    return jsonify(workout.to_dict()), 201


# -----------------------------
# GET ALL WORKOUTS
# -----------------------------
@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify([workout.to_dict() for workout in workouts])

# -----------------------------
# UPDATE WORKOUT
# -----------------------------
@app.route("/workouts/<int:workout_id>", methods=["PUT"])
def update_workout(workout_id):
    workout = Workout.query.get(workout_id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    data = request.get_json()

    workout.workout_type = data.get("workout_type", workout.workout_type)
    workout.duration_minutes = data.get("duration_minutes", workout.duration_minutes)

    db.session.commit()

    return jsonify(workout.to_dict())


# -----------------------------
# DELETE WORKOUT
# -----------------------------
@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = Workout.query.get(workout_id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": "Workout deleted"})


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, session
import datetime
from quotes import quotes

app = Flask(__name__)
app.secret_key = "supersecretkey"

# =========================
# HOME PAGE
# =========================
@app.route("/")
def home():
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    quote = quotes[day_of_year % len(quotes)]
    return render_template("index.html", quote=quote)

# =========================
# RECOMMENDATION PAGE
# =========================
@app.route("/recommend", methods=["POST"])
def recommend():
    # -------- User Details --------
    name = request.form["name"]
    age = int(request.form["age"])
    gender = request.form["gender"]
    height = float(request.form["height"])
    weight = float(request.form["weight"])
    goal = request.form["goal"]
    diet_type = request.form["diet_type"]

    # ---------------- BMI ----------------
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 25:
        bmi_status = "Healthy"
    elif bmi < 30:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"

    # =========================
    # FITNESS SCORE
    # =========================
    if bmi < 18.5:
        fitness = "🟡 Needs Healthy Weight Gain"
    elif bmi < 25:
        fitness = "🟢 Excellent Fitness Range"
    elif bmi < 30:
        fitness = "🟠 Moderate Risk - Improve Fitness"
    else:
        fitness = "🔴 High Health Risk - Lifestyle Changes Recommended"

    # -------- BMR --------
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    # =========================
    # DAILY CALORIE RECOMMENDATION
    # =========================
    if goal == "Weight Loss":
        calories = int(bmr - 500)
        calorie_message = "🔥 Calorie Deficit for Healthy Weight Loss"
    elif goal == "Muscle Gain":
        calories = int(bmr + 300)
        calorie_message = "💪 Calorie Surplus for Muscle Growth"
    else:
        calories = int(bmr)
        calorie_message = "⚖️ Maintenance Calories to Stay Fit"

    # -------- Water --------
    water = "💧 3.7 " if gender == "Male" else "💧 2.7 "

    # -------- Sleep --------
    if age < 18:
        sleep = "😴 8–10 Hours"
    elif age <= 40:
        sleep = "😴 7–9 Hours"
    elif age <= 64:
        sleep = "😴 7–8 Hours"
    else:
        sleep = "😴 6–8 Hours"

    # =========================
    # WORKOUT RECOMMENDATION
    # =========================
    workout = []
    if goal == "Weight Loss":
        if age < 18:
            workout = ["🚶 30 min Walking", "🚴 Cycling", "🤸 Skipping", "🧘 Stretching", "🏃 Light Jogging"]
        elif age <= 40:
            if gender == "Male":
                workout = ["🏋️ Chest Workout", "💪 Back Workout", "🦵 Leg Day", "🏋️ Shoulder Workout", "⚡ Deadlifts"]
            else:
                workout = ["🏋️ Strength Training", "🍑 Glute Workout", "🦵 Leg Workout", "🎗 Resistance Bands", "💪 Core Workout"]
        else:
            workout = ["🌅 Morning Walk", "🧘 Yoga", "🏊 Swimming", "🚶 Light Cardio", "🤸 Stretching"]

    elif goal == "Muscle Gain":
        if age < 18:
            workout = ["💪 Push-ups", "🦵 Squats", "🏋️ Pull-ups", "🏋️ Light Dumbbells", "🎗 Resistance

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

    # -------- BMR --------
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    # -------- Calories --------
    if goal == "Weight Loss":
        calories = int(bmr - 500)
    elif goal == "Muscle Gain":
        calories = int(bmr + 300)
    else:
        calories = int(bmr)

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
            workout = [
                "🚶 30 min Walking",
                "🚴 Cycling",
                "🤸 Skipping",
                "🧘 Stretching",
                "🏃 Light Jogging"
            ]
        elif age <= 40:
            if gender == "Male":
    workout = [
        "🏃 Running",
        "🔥 HIIT Workout",
        "🤸 Jump Rope",
        "🚴 Cycling",
        "💪 Core Workout"
    ]
            else:
    workout = [
        "🚶 Brisk Walk",
        "🔥 HIIT Workout",
        "🧘 Yoga",
        "🚴 Cycling",
        "💪 Bodyweight Training"
    ]
                ]
        else:
            workout = [
                "🌅 Morning Walk",
                "🧘 Yoga",
                "🏊 Swimming",
                "🚶 Light Cardio",
                "🤸 Stretching"
            ]

    elif goal == "Muscle Gain":
        if age < 18:
            workout = [
                "💪 Push-ups",
                "🦵 Squats",
                "🏋️ Pull-ups",
                "🏋️ Light Dumbbells",
                "🎗 Resistance Bands"
            ]
        elif age <= 40:
            if gender == "Male":
                workout = [
                    "🏋️ Chest Workout",
                    "💪 Back Workout",
                    "🦵 Leg Day",
                    "🏋️ Shoulder Workout",
                    "⚡ Deadlifts"
                ]
            else:
                workout = [
                    "🏋️ Strength Training",
                    "🍑 Glute Workout",
                    "🦵 Leg Workout",
                    "🎗 Resistance Bands",
                    "💪 Core Workout"
                ]
        else:
            workout = [
                "🎗 Resistance Bands",
                "🏋️ Light Weights",
                "🚶 Walking",
                "🧘 Yoga",
                "🤸 Mobility Exercises"
            ]

    elif goal == "Stay Fit":
        if age < 18:
            workout = [
                "🏃 Light Jogging",
                "🚴 Cycling",
                "🤸 Skipping",
                "⚽ Outdoor Sports",
                "🧘 Stretching"
            ]
        elif age <= 40:
            if gender == "Male":
                workout = [
                    "🏃 Running",
                    "🏋️ Full Body Workout",
                    "🚴 Cycling",
                    "🧘 Yoga",
                    "💪 Core Training"
                ]
            else:
                workout = [
                    "🚶 Brisk Walking",
                    "🧘 Yoga",
                    "💃 Dance Fitness",
                    "🚴 Cycling",
                    "💪 Pilates"
                ]
        else:
            workout = [
                "🚶 Morning Walk",
                "🧘 Yoga",
                "🤸 Stretching",
                "🏊 Swimming",
                "💨 Breathing Exercises"
            ]

    # -------- Diet --------
    diet = []
    if diet_type == "Vegetarian":
        diet = ["🥛 Milk", "🍎 Fruits", "🥦 Vegetables"]
    else:
        diet = ["🍗 Chicken", "🥚 Eggs", "🐟 Fish"]

    # -------- Save to session --------
    session["name"] = name
    session["age"] = age
    session["gender"] = gender
    session["goal"] = goal
    session["diet_type"] = diet_type
    session["bmi"] = round(bmi, 2)
    session["bmi_status"] = bmi_status
    session["calories"] = calories
    session["water"] = water
    session["sleep"] = sleep
    session["workout"] = workout
    session["diet"] = diet

    return render_template(
        "result1.html",
        name=name,
        age=age,
        gender=gender,
        goal=goal,
        diet_type=diet_type,
        bmi=round(bmi, 2),
        bmi_status=bmi_status,
        calories=calories,
        water=water,
        sleep=sleep,
        workout=workout,
        diet=diet
    )

# =========================
# RESULT PAGES
# =========================
@app.route("/result1")
def result1():
    return render_template("result1.html", **session)

@app.route("/result2")
def result2():
    return render_template("result2.html", **session)

@app.route("/result3")
def result3():
    return render_template("result3.html", **session)

@app.route("/result4")
def result4():
    return render_template("result4.html", **session)

@app.route("/result5")
def result5():
    return render_template("result5.html", **session)

@app.route("/summary")
def summary():
    return render_template("result.html", **session)

# =========================
# CHATBOT
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data["message"].lower()

    if "bmi" in message:
        reply = f"📊 Your BMI is {session.get('bmi')} ({session.get('bmi_status')})."
    elif "calories" in message:
        reply = f"🔥 Your daily calorie target is {session.get('calories')} kcal."
    else:
        reply = "🤖 I can answer questions about your diet, workout, BMI, calories, water or sleep."

    return {"reply": reply}

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)

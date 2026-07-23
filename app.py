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

    # -------- Weight Loss --------
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

        else:
            workout = [
                "🌅 Morning Walk",
                "🧘 Yoga",
                "🏊 Swimming",
                "🚶 Light Cardio",
                "🤸 Stretching"
            ]

    # -------- Muscle Gain --------
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

    # -------- Stay Fit --------
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

    # Greetings
    if any(word in message for word in ["hi", "hello", "hey"]):
        reply = f"Hello {session.get('name','')}! 👋 I'm Nexora. Ask me about your workout, diet, BMI, calories, sleep or water."

    elif "how are you" in message or "how are u" in message:
        reply = "😊 I'm doing great! I'm ready to help with your fitness journey."

    elif "thank" in message:
        reply = "You're welcome! 💙 Stay healthy."

    # BMI
    elif "bmi" in message:
        reply = f"📊 Your BMI is {session.get('bmi')} ({session.get('bmi_status')})."

    # Calories
    elif "calorie" in message or "calories" in message:
        reply = f"🔥 Your recommended daily calories are {session.get('calories')} kcal."

    # Water
    elif "water" in message or "drink" in message:
        reply = f"💧 Recommended water intake: {session.get('water')} litres per day."

    # Sleep
    elif "sleep" in message or "rest" in message:
        reply = f"😴 Recommended sleep: {session.get('sleep')}."

    # Workout
    elif "workout" in message or "exercise" in message:
        reply = "💪 Your workout plan includes:<br>" + "<br>".join(session.get("workout", []))

    # Diet
    elif "diet" in message or "food" in message:
        reply = "🥗 Your recommended diet includes:<br>" + "<br>".join(session.get("diet", []))

    # Walking
    elif "walking" in message:
        reply = "🚶 Walking for 30-45 minutes daily is recommended for general fitness."

    # Running
    elif "running" in message or "jogging" in message:
        reply = "🏃 Beginners should start with 20-30 minutes of running or jogging, 3-5 days a week."

    # Cycling
    elif "cycling" in message or "cycle" in message:
        reply = "🚴 Cycling for about 30-45 minutes (or 8-15 km) is a great workout. Beginners can start with 3-4 sessions per week."

    # Pushups
    elif "push" in message:
        reply = "💪 Beginners can start with 8-12 push-ups for 2-3 sets."

    # Squats
    elif "squat" in message:
        reply = "🦵 Beginners should try 10-15 squats for 2-3 sets."

    # Yoga
    elif "yoga" in message:
        reply = "🧘 20-30 minutes of yoga daily helps improve flexibility and reduces stress."

    # Protein
    elif "protein" in message:
        reply = "🥚 Protein helps build and repair muscles. Include eggs, chicken, fish, milk, beans or paneer."

    # Weight loss
    elif "weight loss" in message:
        reply = "🔥 Weight loss works best with calorie deficit, regular cardio, strength training and healthy eating."

    # Muscle gain
    elif "muscle" in message:
        reply = "💪 For muscle gain, focus on strength training, protein-rich food and proper sleep."

    else:
        reply = (
            "🤖 I don't know that yet.<br><br>"
            "Try asking:<br>"
            "• What is my BMI?<br>"
            "• Show my workout<br>"
            "• Show my diet<br>"
            "• How much water should I drink?<br>"
            "• How many calories do I need?<br>"
            "• How long should I sleep?<br>"
            "• Is cycling good?<br>"
            "• How many pushups should I do?"
        )

    return {"reply": reply}
# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)

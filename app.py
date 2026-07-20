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

    elif goal == "Stay Fit":
        calories = int(bmr)
        calorie_message = "⚖️ Maintenance Calories to Stay Fit"

    # -------- Water --------
    if gender == "Male":
        water = "💧 3.7 "
    else:
        water = "💧 2.7 "

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
        
       # =========================
    # DIET RECOMMENDATION
    # =========================

    diet = []

    # -------- Vegetarian --------
    if diet_type == "Vegetarian":

        if goal == "Weight Loss":

            if age < 18:
                diet = [
                    "🥣 Oats",
                    "🍎 Fruits",
                    "🌱 Sprouts",
                    "🍲 Dal",
                    "🥦 Green Vegetables"
                ]

            elif age <= 40:
                diet = [
                    "🍚 Brown Rice",
                    "🧀 Paneer",
                    "🍲 Dal",
                    "🥦 Vegetables",
                    "🍎 Fruits",
                    "🌱 Sprouts"
                ]

            else:
                diet = [
                    "🥣 Vegetable Soup",
                    "🥛 Curd",
                    "🫓 Chapati",
                    "🥦 Steamed Vegetables",
                    "🍎 Fruits"
                ]

        elif goal == "Muscle Gain":

            if age < 18:
                diet = [
                    "🥛 Milk",
                    "🧀 Paneer",
                    "🌱 Soy Chunks",
                    "🍌 Banana",
                    "🥜 Peanut Butter"
                ]

            elif age <= 40:

                if gender == "Male":
                    diet = [
                        "🧀 Paneer",
                        "🥛 Milk",
                        "🌱 Soy Chunks",
                        "🍲 Tofu",
                        "🍛 Lentils",
                        "🍌 Banana",
                        "🥜 Peanut Butter"
                    ]

                else:
                    diet = [
                        "🍲 Tofu",
                        "🌱 Soy Chunks",
                        "🧀 Paneer",
                        "🍛 Lentils",
                        "🥜 Mixed Nuts",
                        "🍌 Banana"
                    ]

            else:
                diet = [
                    "🥛 Curd",
                    "🧀 Paneer",
                    "🥛 Milk",
                    "🥦 Vegetables",
                    "🥜 Nuts"
                ]

        # -------- Stay Fit --------
        elif goal == "Stay Fit":

            if age < 18:
                diet = [
                    "🥛 Milk",
                    "🍎 Fruits",
                    "🍲 Dal",
                    "🥦 Vegetables",
                    "🫓 Chapati"
                ]

            elif age <= 40:
                diet = [
                    "🫓 Whole Wheat Chapati",
                    "🥦 Green Vegetables",
                    "🥛 Curd",
                    "🍎 Fruits",
                    "🥜 Nuts",
                    "🍚 Brown Rice"
                ]

            else:
                diet = [
                    "🥣 Vegetable Soup",
                    "🥛 Curd",
                    "🥦 Steamed Vegetables",
                    "🍎 Fruits",
                    "🥜 Almonds"
                ]

    # -------- Non-Vegetarian --------
    else:

if age < 18:
    diet = [
        "🥚 Boiled Eggs",
        "🍗 Grilled Chicken",
        "🥗 Salad",
        "🥦 Vegetables"
    ]

elif age <= 40:
    diet = [
        "🍗 Grilled Chicken",
        "🐟 Fish",
        "🥦 Vegetables",
        "🍚 Brown Rice",
        "🥗 Salad"
    ]

            else:
                diet = [
                    "🐟 Fish Curry",
                    "🍗 Steamed Chicken",
                    "🥦 Vegetables",
                    "🥣 Soup"
                ]

        elif goal == "Muscle Gain":

            if age < 18:
                diet = [
                    "🥚 Eggs",
                    "🥛 Milk",
                    "🍗 Chicken",
                    "🍚 Rice",
                    "🍌 Banana"
                ]

            elif age <= 40:

                if gender == "Male":
                    diet = [
                        "🍗 Chicken Breast",
                        "🥚 Eggs",
                        "🐟 Fish",
                        "🍖 Lean Meat",
                        "🥛 Milk",
                        "🍚 Rice",
                        "🍌 Banana"
                    ]

                else:
                    diet = [
                        "🥚 Eggs",
                        "🐟 Fish",
                        "🍗 Chicken",
                        "🥛 Milk",
                        "🥦 Vegetables",
                        "🥜 Nuts"
                    ]

            else:
                diet = [
                    "🥚 Eggs",
                    "🐟 Fish",
                    "🍗 Chicken Soup",
                    "🥦 Vegetables",
                    "🍚 Rice"
                ]

        # -------- Stay Fit --------
        elif goal == "Stay Fit":

            if age < 18:
                diet = [
                    "🥚 Eggs",
                    "🥛 Milk",
                    "🍗 Chicken",
                    "🍎 Fruits",
                    "🥦 Vegetables"
                ]

            elif age <= 40:
                diet = [
                    "🍗 Grilled Chicken",
                    "🐟 Fish",
                    "🥚 Eggs",
                    "🥦 Vegetables",
                    "🍚 Brown Rice",
                    "🍎 Fruits"
                ]

            else:
                diet = [
                    "🐟 Fish",
                    "🍗 Chicken Soup",
                    "🥦 Vegetables",
                    "🥣 Soup",
                    "🍎 Fruits"
                ]
      # =========================
    # SAVE TO SESSION
    # =========================

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

    # =========================
    # RESULT PAGE
    # =========================

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
    @app.route("/result1")
def result1():
    return render_template(
        "result1.html",
        name=session.get("name"),
        bmi=session.get("bmi"),
        bmi_status=session.get("bmi_status"),
        goal=session.get("goal"),
        calories=session.get("calories")
    )


@app.route("/result2")
def result2():
    return render_template(
        "result2.html",
        goal=session.get("goal"),
        calories=session.get("calories")
    )


@app.route("/result3")
def result3():
    return render_template(
        "result3.html",
        workout=session.get("workout")
    )


@app.route("/result4")
def result4():
    return render_template(
        "result4.html",
        diet=session.get("diet")
    )


@app.route("/result5")
def result5():
    return render_template(
        "result5.html",
        water=session.get("water"),
        sleep=session.get("sleep")
    )


@app.route("/summary")
def summary():
    return render_template(
        "summary.html",
        name=session.get("name"),
        bmi=session.get("bmi"),
        bmi_status=session.get("bmi_status"),
        goal=session.get("goal"),
        calories=session.get("calories"),
        workout=session.get("workout"),
        diet=session.get("diet"),
        water=session.get("water"),
        sleep=session.get("sleep")
    )


# =========================
# AI CHATBOT
# =========================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    message = data["message"].lower()

    age = session.get("age")
    gender = session.get("gender")
    diet_type = session.get("diet_type")
    goal = session.get("goal")
    workout = session.get("workout", [])
    diet = session.get("diet", [])
    bmi = session.get("bmi")
    calories = session.get("calories")

    if "protein" in message:

        if diet_type == "Vegetarian":
            reply = (
                "🥛 Good vegetarian protein sources are Paneer, Soy Chunks, "
                "Tofu, Lentils, Milk and Peanut Butter."
            )

        else:
            reply = (
                "🍗 Good protein sources are Chicken, Eggs, Fish, Lean Meat "
                "and Milk."
            )

    elif "diet" in message:
        reply = "🥗 Your recommended diet is: " + ", ".join(diet)

    elif "workout" in message or "exercise" in message:
        reply = "💪 Your recommended workout is: " + ", ".join(workout)

    elif "water" in message:
        reply = f"💧 Drink around {session.get('water')} every day."

    elif "sleep" in message:
        reply = f"😴 Recommended sleep: {session.get('sleep')}."

    elif "bmi" in message:
    reply = f"📊 Your BMI is {bmi} ({session.get('bmi_status')})."

    elif "calories" in message:
    reply = f"🔥 Your daily calorie target is approximately {calories} kcal."

    elif "goal" in message:
        reply = f"🎯 Your selected goal is {goal}."

    elif "hello" in message or "hi" in message:
        reply = f"👋 Hello {session.get('name')}! How can I help you today?"

    else:
        reply = (
            "🤖 I can answer questions about your "
            "diet 🍽️, workout 💪, BMI 📊, "
            "calories 🔥, water 💧 or sleep 😴."
        )

    return {"reply": reply}


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "supersecretkey"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():

    name = request.form["name"]
    age = int(request.form["age"])
    gender = request.form["gender"]
    height = float(request.form["height"])
    weight = float(request.form["weight"])
    goal = request.form["goal"]
    diet_type = request.form["diet_type"]

    session["user_context"] = {
        "name": name,
        "age": age,
        "gender": gender,
        "diet_type": diet_type,
        "goal": goal
    }

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

    # ---------------- BMR ----------------
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    # ---------------- Calories ----------------
    if goal == "Weight Loss":
        calories = int(bmr - 500)
    elif goal == "Muscle Gain":
        calories = int(bmr + 300)
    else:
        calories = int(bmr)

    # ---------------- Water ----------------
    if gender == "Male":
        water = "3.7 Litres/day"
    else:
        water = "2.7 Litres/day"

    # ---------------- Sleep ----------------
    if age < 18:
        sleep = "8-10 hours"
    elif age <= 40:
        sleep = "7-9 hours"
    elif age <= 64:
        sleep = "7-8 hours"
    else:
        sleep = "6-8 hours"

    # ---------------- Workout ----------------
    workout = []
    if goal == "Weight Loss":
        if age < 18:
            workout = ["30 min Walking", "Cycling", "Skipping", "Stretching", "Light Jogging"]
        elif age <= 40:
            if gender == "Male":
                workout = ["Running", "HIIT", "Jump Rope", "Cycling", "Core Workout"]
            else:
                workout = ["Brisk Walk", "HIIT", "Yoga", "Cycling", "Bodyweight Training"]
        else:
            workout = ["Morning Walk", "Yoga", "Swimming", "Light Cardio", "Stretching"]

    elif goal == "Muscle Gain":
        if age < 18:
            workout = ["Push-ups", "Squats", "Pull-ups", "Light Dumbbells", "Resistance Bands"]
        elif age <= 40:
            if gender == "Male":
                workout = ["Chest Workout", "Back Workout", "Leg Day", "Shoulders", "Deadlifts"]
            else:
                workout = ["Strength Training", "Glute Workout", "Leg Workout", "Resistance Training", "Core Workout"]
        else:
            workout = ["Resistance Bands", "Light Weights", "Walking", "Yoga", "Mobility Exercises"]

    else:
        workout = ["Walking", "Yoga", "Cycling", "Stretching", "Meditation"]

    # ---------------- Diet (Age + Gender + Type + Goal) ----------------
    diet = []
    if diet_type == "Vegetarian":
        if goal == "Weight Loss":
            if age < 18:
                diet = ["Oats", "Fruits", "Sprouts", "Dal", "Green Vegetables"]
            elif age <= 40:
                diet = ["Brown Rice", "Paneer", "Dal", "Vegetables", "Fruits", "Sprouts"]
            else:
                diet = ["Vegetable Soup", "Curd", "Chapati", "Steamed Veggies", "Fruits"]
        elif goal == "Muscle Gain":
            if age < 18:
                diet = ["Milk", "Paneer", "Soy Chunks", "Banana", "Peanut Butter"]
            elif age <= 40:
                if gender == "Male":
                    diet = ["Paneer", "Milk", "Soy Chunks", "Tofu", "Lentils", "Banana", "Peanut Butter"]
                else:
                    diet = ["Tofu", "Soy Chunks", "Paneer", "Lentils", "Nuts", "Banana"]
            else:
                diet = ["Curd", "Paneer", "Milk", "Vegetables", "Nuts"]
        else:
            diet = ["Chapati", "Vegetables", "Curd", "Fruits", "Nuts"]

    else:  # Non-Vegetarian
        if goal == "Weight Loss":
            if age < 18:
                diet = ["Boiled Eggs", "Grilled Chicken", "Salad", "Vegetables"]
            elif age <= 40:
                diet = ["Grilled Chicken", "Fish", "Vegetables", "Brown Rice", "Salad"]
            else:
                diet = ["Fish Curry", "Steamed Chicken", "Vegetables", "Soup"]
        elif goal == "Muscle Gain":
            if age < 18:
                diet = ["Eggs", "Milk", "Chicken", "Rice", "Banana"]
            elif age <= 40:
                if gender == "Male":
                    diet = ["Chicken Breast", "Eggs", "Fish", "Lean Meat", "Milk", "Rice", "Banana"]
                else:
                    diet = ["Eggs", "Fish", "Chicken", "Milk", "Vegetables", "Nuts"]
            else:
                diet = ["Eggs", "Fish", "Chicken Soup", "Vegetables", "Rice"]
        else:
            diet = ["Eggs", "Chicken", "Fish", "Vegetables", "Whole Wheat"]

    # ---------------- Result Page ----------------
    return render_template(
        "result1.html",
        name=name,
        bmi=round(bmi, 2),
        bmi_status=bmi_status,
        calories=calories,
        workout=workout,
        diet=diet,
        water=water,
        sleep=sleep,
        goal=goal
    )


# ---------------- CHATBOT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data["message"].lower()
    context = session.get("user_context", {})

    if "protein" in user_message:
        if context.get("diet_type") == "Vegetarian":
            reply = "Best vegetarian protein sources are Paneer, Soy Chunks, Tofu, Milk, Lentils, Chickpeas and Sprouts."
        else:
            reply = "Best non-vegetarian protein sources are Eggs, Chicken, Fish and Lean Meat."

    elif "water" in user_message:
        if context.get("gender") == "Male":
            reply = "Drink around 3.7 litres of water daily."
        else:
            reply = "Drink around 2.7 litres of water daily."

    elif "sleep" in user_message:
        age = context.get("age", 20)
        if age < 18:
            reply = "You should sleep 8-10 hours every night."
        elif age <= 40:
            reply = "You should sleep 7-9 hours every night."
        elif age <= 64:
            reply = "You should sleep 7-8 hours every night."
        else:
            reply = "You should sleep 6-8 hours every night."

    elif "diet" in user_message:
        if context.get("diet_type") == "Vegetarian":
            reply = "Follow a vegetarian diet rich in paneer, tofu, dal, sprouts and vegetables."
        else:
            reply = "Follow a protein-rich diet including eggs, chicken and fish."

    elif "workout" in user_message:
        goal = context.get("goal")
        if goal == "Weight Loss":
            reply = "Focus on cardio, HIIT, walking and cycling."
        elif goal == "Muscle Gain":
            reply = "Focus on strength training and progressive overload."
        else:
            reply = "Walking, stretching and yoga are ideal."

    elif "bmi" in user_message:
        reply = "BMI is calculated using weight divided by height squared."

    else:
        reply = "Ask me about Diet, Workout, Water, Sleep, BMI or Calories."

    return {"reply": reply}


if __name__ == "__main__":
    app.run(debug=True)

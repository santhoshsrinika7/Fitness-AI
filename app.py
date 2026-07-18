from flask import Flask, render_template, request, session
import datetime
from quotes import quotes

@app.route("/")
def home():
    # pick quote based on day of year
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    quote = quotes[day_of_year % len(quotes)]  # safe wrap-around

    return render_template("index.html", quote=quote)


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
    water = "3.7 Litres/day" if gender == "Male" else "2.7 Litres/day"

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

    # ---------------- Diet ----------------
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

    # ---------------- Save to session ----------------
    session["name"] = name
    session["age"] = age
    session["gender"] = gender
    session["goal"] = goal
    session["diet_type"] = diet_type
    session["bmi"] = round(bmi, 2)
    session["bmi_status"] = bmi_status
    session

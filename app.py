from flask import Flask, render_template, request

app = Flask(__name__)

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

    # BMI
    bmi = weight / ((height / 100) ** 2)

    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 25:
        bmi_status = "Healthy"
    elif bmi < 30:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"

    # BMR
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    if goal == "Weight Loss":
        calories = int(bmr - 500)
        workout = [
            "30 Minutes Walking",
            "Jogging",
            "Cycling",
            "Jump Rope",
            "HIIT Workout"
        ]
        diet = [
            "Oats",
            "Salad",
            "Boiled Eggs",
            "Grilled Chicken / Paneer",
            "Fruits"
        ]

    elif goal == "Muscle Gain":
        calories = int(bmr + 300)
        workout = [
            "Push-ups",
            "Squats",
            "Bench Press",
            "Deadlift",
            "Pull-ups"
        ]
        diet = [
            "Milk",
            "Eggs",
            "Chicken / Paneer",
            "Rice",
            "Banana"
        ]

    else:
        calories = int(bmr)
        workout = [
            "Walking",
            "Yoga",
            "Stretching",
            "Light Strength Training"
        ]
        diet = [
            "Balanced Diet",
            "Vegetables",
            "Fruits",
            "Whole Grains"
        ]

    water = round(weight * 0.035, 2)

    if age < 18:
        sleep = "8-10 Hours"
    elif age <= 64:
        sleep = "7-9 Hours"
    else:
        sleep = "7-8 Hours"

    return render_template(
        "result.html",
        name=name,
        bmi=round(bmi,2),
        bmi_status=bmi_status,
        calories=calories,
        workout=workout,
        diet=diet,
        water=water,
        sleep=sleep,
        goal=goal
    )

if __name__ == "__main__":
    app.run(debug=True)

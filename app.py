from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session storage

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

    # Store user context in session for chatbot
    session["user_context"] = {
        "name": name,
        "age": age,
        "gender": gender,
        "diet_type": diet_type,
        "goal": goal
    }

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

    # Calories based on goal
    if goal == "Weight Loss":
        calories = int(bmr - 500)
    elif goal == "Muscle Gain":
        calories = int(bmr + 300)
    else:
        calories = int(bmr)

    # Workout + Diet logic (same as your current version)
    # ... [your existing workout/diet code here] ...

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

# 🟢 Chatbot Route
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"].lower()
    context = session.get("user_context", {})

    # Personalized replies using context
    if "protein" in user_message:
        if context.get("diet_type") == "Vegetarian":
            reply = f"Since you’re a {context.get('age')}-year-old {context.get('gender').lower()} vegetarian, paneer, soybeans, and lentils are excellent protein sources."
        else:
            reply = f"Since you’re a {context.get('age')}-year-old {context.get('gender').lower()} non-vegetarian, eggs, chicken, and fish are great protein sources."
    elif "water" in user_message:
        if context.get("gender") == "Male":
            reply = "Men generally need about 3.7 L of water daily."
        else:
            reply = "Women generally need about 2.7 L of water daily."
    elif "sleep" in user_message:
        if context.get("age") < 18:
            reply = "Teens need 8–10 hours of sleep."
        elif context.get("age") <= 40:
            reply = "Adults need 7–9 hours of sleep."
        elif context.get("age") <= 64:
            reply = "Middle-aged adults need 7–8 hours of sleep."
        else:
            reply = "Seniors need 6–8 hours of sleep."
    elif "workout" in user_message:
        reply = f"For your age group ({context.get('age')}), focus on {', '.join(workout)}."
    elif "diet" in user_message:
        reply = f"Your recommended diet includes: {', '.join(diet)}."
    else:
        reply = "I can help with diet, workout, water, sleep, or BMI questions!"

    return {"reply": reply}

if __name__ == "__main__":
    app.run(debug=True)

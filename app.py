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
# AI FITNESS CHATBOT
# =========================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data["message"].lower()


    name = session.get("name","User")
    bmi = session.get("bmi")
    bmi_status = session.get("bmi_status")
    calories = session.get("calories")
    workout = session.get("workout",[])
    diet = session.get("diet",[])
    water = session.get("water")
    sleep = session.get("sleep")
    goal = session.get("goal")



    # ---------------- GREETINGS ----------------

    if any(word in message for word in ["hi","hello","hey","hii"]):

        reply = f"""
        Hello {name}! 👋😊

        I am Nexora AI Fitness Assistant.

        I can help you with:
        🏋️ Workout plans
        🥗 Diet suggestions
        📊 BMI analysis
        🔥 Calories
        💧 Water intake
        😴 Sleep
        💪 Fitness tips

        Ask me anything!
        """



    # ---------------- PERSONAL REPORT ----------------


    elif "my report" in message or "summary" in message:

        reply = f"""
        📄 Your Fitness Summary:

        📊 BMI: {bmi}
        Status: {bmi_status}

        🎯 Goal:
        {goal}

        🔥 Daily Calories:
        {calories} kcal

        💧 Water:
        {water} litres/day

        😴 Sleep:
        {sleep}

        Keep following your plan consistently! 💙
        """



    # ---------------- BMI ----------------


    elif "bmi" in message or "weight status" in message:

        if bmi_status == "Healthy":

            advice="Your BMI is in a healthy range. Maintain your current lifestyle."

        elif bmi_status=="Underweight":

            advice="Try increasing healthy calories and include protein-rich foods."

        elif bmi_status=="Overweight":

            advice="Focus on regular workouts, balanced diet and calorie control."

        else:

            advice="Consider improving activity levels and following a healthy eating plan."


        reply=f"""
        📊 BMI Analysis:

        Your BMI: {bmi}

        Category:
        {bmi_status}

        AI Advice:
        {advice}
        """



    # ---------------- CALORIES ----------------


    elif "calorie" in message or "energy" in message:

        reply=f"""
        🔥 Your Daily Calorie Requirement:

        {calories} kcal/day

        This is calculated using:
        ✔ Age
        ✔ Gender
        ✔ Height
        ✔ Weight
        ✔ Fitness Goal

        Remember: Calories should come from nutritious foods.
        """



    # ---------------- WORKOUT ----------------


    elif any(word in message for word in 
             ["workout","exercise","training","gym"]):

        reply="""
        💪 Your Personalized Workout Plan:

        """ + "<br>".join(workout) + """

        Tips:
        ✅ Warm up before exercise
        ✅ Stay consistent
        ✅ Increase intensity slowly
        """



    # ---------------- DIET ----------------


    elif any(word in message for word in
             ["diet","food","eat","meal"]):

        reply="""
        🥗 Your Recommended Diet:

        """ + "<br>".join(diet) + """

        Healthy Eating Tips:

        🥦 Include vegetables
        🍎 Eat fruits daily
        💧 Drink enough water
        🥚 Maintain protein intake
        """



    # ---------------- WATER ----------------


    elif "water" in message or "hydration" in message:

        reply=f"""
        💧 Hydration Recommendation:

        Your recommended intake:
        {water} litres/day

        Tip:
        Drink water throughout the day instead of drinking a lot at once.
        """



    # ---------------- SLEEP ----------------


    elif "sleep" in message or "rest" in message:

        reply=f"""
        😴 Sleep Recommendation:

        {sleep}

        Good sleep helps:
        ✔ Muscle recovery
        ✔ Better concentration
        ✔ Energy levels
        """



    # ---------------- FITNESS QUESTIONS ----------------


    elif "protein" in message:

        reply="""
        🥚 Protein helps your body repair and build muscles.

        Sources:
        Vegetarian:
        🥛 Milk
        🫘 Beans
        🧀 Paneer

        Non-Vegetarian:
        🍗 Chicken
        🥚 Eggs
        🐟 Fish
        """



    elif "weight loss" in message:

        reply="""
        🔥 Weight Loss Tips:

        ✅ Maintain calorie balance
        ✅ Do cardio + strength training
        ✅ Eat enough protein
        ✅ Sleep properly
        ✅ Stay consistent

        Small daily improvements create big results.
        """



    elif "muscle" in message or "muscle gain" in message:

        reply="""
        💪 Muscle Gain Tips:

        ✅ Strength training
        ✅ Protein-rich diet
        ✅ Progressive overload
        ✅ Proper recovery
        ✅ 7-9 hours sleep
        """



    elif "motivate" in message or "motivation" in message:

        reply="""
        🚀 Remember:

        Fitness is not about being perfect.
        It is about improving yourself every day.

        One workout. One healthy meal.
        One step closer to your goal. 💙
        """



    # ---------------- DEFAULT ----------------


    else:

        reply="""
        🤖 I can help you with:

        📊 What is my BMI?
        🔥 How many calories do I need?
        🏋️ Show my workout
        🥗 Show my diet
        💧 How much water should I drink?
        😴 How much sleep do I need?
        💪 Give fitness tips
        🔥 Help me lose weight

        Try asking me something!
        """

    return {"reply": reply}
# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)

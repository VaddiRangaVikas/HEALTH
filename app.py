from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Symptom risk weights
symptom_weights = {
    "fever": 20,
    "cough": 10,
    "headache": 5,
    "vomiting": 15,
    "fatigue": 10,
    "chest pain": 40,
    "breathing difficulty": 50
}

# Risk calculation function
def calculate_risk(symptoms):

    score = 0
    detected = []

    for symptom in symptoms:

        symptom = symptom.lower().strip()

        if symptom in symptom_weights:
            score += symptom_weights[symptom]
            detected.append(symptom)

    # Risk classification
    if score <= 25:
        risk = "Low"
        recommendation = "Self Care"

    elif score <= 50:
        risk = "Moderate"
        recommendation = "Consult Doctor Online"

    elif score <= 75:
        risk = "High"
        recommendation = "Visit Hospital"

    else:
        risk = "Critical"
        recommendation = "Seek Emergency Care Immediately"

    return score, risk, recommendation, detected


# Home route
@app.route("/")
def home():
    return render_template("index.html")


# Prediction API
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    symptoms = data.get("symptoms", [])

    score, risk, recommendation, detected = calculate_risk(symptoms)

    return jsonify({
        "risk_score": score,
        "risk_level": risk,
        "recommendation": recommendation,
        "explanation": detected
    })


if __name__ == "__main__":
    app.run(debug=True)

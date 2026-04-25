from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import csv
import os

app = Flask(__name__)

# -----------------------------
# MongoDB Connection
# -----------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["survey_db"]
collection = db["users"]

# -----------------------------
# Ensure CSV folder exists
# -----------------------------
if not os.path.exists("data"):
    os.makedirs("data")

csv_file = "data/users.csv"

# Create CSV header if file doesn't exist
if not os.path.isfile(csv_file):
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Age", "Gender", "Income",
            "Utilities", "Entertainment",
            "School Fees", "Shopping", "Healthcare"
        ])

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def home():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():

    # User inputs
    age = int(request.form['age'])
    gender = request.form['gender']
    income = float(request.form['income'])

    utilities = float(request.form.get('utilities', 0))
    entertainment = float(request.form.get('entertainment', 0))
    school_fees = float(request.form.get('school_fees', 0))
    shopping = float(request.form.get('shopping', 0))
    healthcare = float(request.form.get('healthcare', 0))

    # -----------------------------
    # Store in MongoDB
    # -----------------------------
    user_data = {
        "age": age,
        "gender": gender,
        "income": income,
        "expenses": {
            "utilities": utilities,
            "entertainment": entertainment,
            "school_fees": school_fees,
            "shopping": shopping,
            "healthcare": healthcare
        }
    }

    collection.insert_one(user_data)

    # -----------------------------
    # Store in CSV
    # -----------------------------
    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            age, gender, income,
            utilities, entertainment,
            school_fees, shopping, healthcare
        ])

    return redirect('/')


# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)

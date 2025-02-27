from flask import Flask, request, jsonify
from flask_cors import CORS  # Додаємо CORS
import json
import os
from datetime import datetime, timedelta
import re

app = Flask(__name__)
CORS(app)  # Дозволяємо CORS для всіх запитів

DATA_FILE = "data.json"

# Функція для завантаження даних
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"attempts": [], "freezes": 0, "last_entry": None}  # Видалено "streak"

# Функція для збереження даних
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/submit", methods=["POST"])
def submit():
    data = load_data()
    today = datetime.today().strftime("%Y-%m-%d")
    
    # Якщо на сьогодні вже є запис – повертаємо помилку
    if today == data["last_entry"]:
        return jsonify({"message": "Сьогодні вже введені дані!"}), 400

    entry = request.json
    data["attempts"].append(parse_exported(str(entry)))  # Зберігаємо запис
    streak = len(data["attempts"])  # Стрік рахується по довжині attempts
    
    if data["last_entry"]:
        last_date = datetime.strptime(data["last_entry"], "%Y-%m-%d")
        
        days_missed = (datetime.today() - last_date).days
        
        if days_missed > data["freezes"] + 1:
            # Якщо минув день після останнього можливого дня – обнуляємо стрік і очищаємо записи
            data["attempts"] = []
            streak = 1
            data["freezes"] = 0  
        else:
            # Витрачаємо рівно стільки заморозок, скільки потрібно
            data["freezes"] -= max(0, days_missed - 1)
    
    # Раз на 4 дні стріку додається 1 заморозка
    if streak % 4 == 0:
        data["freezes"] += 1

    roll_datas(data)
    save_data(data)

    return jsonify({"message": "Дані збережено!", "streak": streak, "freezes": data["freezes"]})

def parse_exported(content):
    # Знайдемо всі часи збірки за допомогою регулярного виразу
    times = re.findall(r'\d+\.\d{2}', content)
    return round(
        sum(float(time) for time in times) 
        / len(times)
        , 2)

def roll_datas(data: dict, direction=""):
    if direction == "back":
        data["last_entry"] = data["previous_datas"][0]
        data["previous_datas"][0] = data["previous_datas"][1]
        data["previous_datas"][1] = ""
    else:   # якщо аргументу нема то вперед, за замовчуванням
        data["previous_datas"][1] = data["previous_datas"][0]
        data["previous_datas"][0] = data["last_entry"]
        data["last_entry"] = datetime.today().strftime("%Y-%m-%d")
    save_data(data)

@app.route("/status", methods=["GET"])
def get_status():
    data = load_data()
    streak = len(data["attempts"])  # Стрік рахується по довжині attempts
    
    reset_day = None
    if data["last_entry"]:
        last_date = datetime.strptime(data["last_entry"], "%Y-%m-%d")
        last_possible_day = last_date + timedelta(days=data["freezes"])
        reset_day = (last_possible_day + timedelta(days=1)).strftime("%Y-%m-%d")
        lost_day = (last_possible_day + timedelta(days=2)).strftime("%Y-%m-%d")

    return jsonify({
        "streak": streak,
        "freezes": data["freezes"],
        "reset_day": reset_day,  # Показуємо дату reset day
        "lost_day": lost_day
    })

@app.route('/get_chart_data', methods=['GET'])
def get_data():
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
    
    return jsonify([float(entry) for entry in data["attempts"]])

@app.route("/cancel", methods=["POST"])
def cancel():
    data = load_data()

    # віднімаємо 1 замороження якщо воно додавалось
    if len(data["attempts"]) % 4 == 0:
        data["freezes"] -= 1
    # видаляємо останній елемент
    data["attempts"].pop()
    # повертаємо стару дату
    roll_datas(data, "back")

    save_data(data)


if __name__ == "__main__":
    app.run(debug=True)

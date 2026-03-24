from flask import Flask, render_template, request, jsonify
from controller.inputManager import InputManager
from db.init_db import init_db


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/search", methods=["POST"])
def search():
    city = request.form.get("city")
    start = request.form.get("start_date")
    end = request.form.get("end_date")
    result = InputManager.search(city, start, end)

    print(result)  # debug

    return jsonify(result)


@app.route("/insert", methods=["POST"])
def insert():
    city = request.form.get("city")
    date = request.form.get("date")
    temperature = request.form.get("temperature")
    result = InputManager.insert(city, date, temperature)
    print(result)  
    return result["message"]

@app.before_first_request
def setup():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)
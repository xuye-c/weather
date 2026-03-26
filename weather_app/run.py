from flask import Flask, request, jsonify, session
from controller.inputManager import InputManager
from configs.messageManager import MessageManager
from db.init_db import init_db
from service.weather_api import WeatherAPI

msg = MessageManager()
app = Flask(__name__)
app.secret_key = 'abcd1234'

@app.before_request
def setup_before_request():
    """每次请求前执行，确保用户语言设置"""
    user_lang = session.get('lang')
    if user_lang and user_lang in msg.get_available_languages():
        msg.set_language(user_lang)

@app.route("/api/set_language", methods=["POST"])
def set_language():
    lang = request.json.get("lang")
    session["lang"] = lang   
    msg.set_language(lang)
    return jsonify({"success": True})

@app.route('/')
def home():
    # 返回API说明，而不是渲染模板
    return jsonify({
        "message": "Weather API Server",
        "endpoints": {
            "insert": "POST /api/insert",
            "search": "POST /api/search", 
            "update": "POST /api/update",
            "delete": "POST /api/delete",
            "set_language": "POST /api/set_language"
        }
    })

@app.route("/api/update", methods=["POST"])
def update():
    city = request.form.get("city")
    date = request.form.get("date")
    temperature = request.form.get("temperature")
    result = InputManager.update(city, date, temperature)
    return jsonify(result)

@app.route("/api/delete", methods=["POST"])
def delete():
    city = request.form.get("city")
    date = request.form.get("date")
    result = InputManager.delete(city, date)
    return jsonify(result)

@app.route("/api/search", methods=["POST"])
def search():
    city = request.form.get("city")
    start = request.form.get("start_date")
    end = request.form.get("end_date")
    db_result = InputManager.search(city, start, end)
    weather_result = WeatherAPI.get_current_weather(city)
    return jsonify({
        "db": db_result,
        "weather": weather_result
    })

@app.route("/api/insert", methods=["POST"])
def insert():
    city = request.form.get("city")
    date = request.form.get("date")
    temperature = request.form.get("temperature")
    result = InputManager.insert(city, date, temperature)
    return jsonify(result)

@app.before_first_request
def setup():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)
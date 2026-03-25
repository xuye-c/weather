from flask import Flask, render_template, request, jsonify, session
from controller.inputManager import InputManager
from configs.messageManager import MessageManager
from db.init_db import init_db

msg = MessageManager()
app = Flask(__name__)
app.secret_key = 'abcd1234'

@app.before_request
def setup_before_request():
    """每次请求前执行，确保用户语言设置"""
    user_lang = session.get('lang')
    if user_lang and user_lang in msg.get_available_languages():
        msg.set_language(user_lang)

@app.route("/set_language", methods=["POST"])
def set_language():
    lang = request.json.get("lang")

    session["lang"] = lang   
    msg.set_language(lang)

    return jsonify({"success": True})

@app.route('/')
def home():
    return render_template(
        "index.html",
        msg = msg,
        languages=msg.get_available_languages(),
        current_lang=msg.get_language()
    )

@app.route("/update", methods=["POST"])
def update():
    city = request.form.get("city")
    date = request.form.get("date")
    temperature = request.form.get("temperature")

    result = InputManager.update(city, date, temperature)
    return result["message"]


@app.route("/delete", methods=["POST"])
def delete():
    city = request.form.get("city")
    date = request.form.get("date")

    result = InputManager.delete(city, date)
    return result["message"]

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
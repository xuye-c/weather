from flask import Flask, request, jsonify, session, Response
from controller.inputManager import InputManager
from configs.messageManager import MessageManager
from db.init_db import init_db
from service.weather_api import WeatherAPI
from service.export import export_manager
from service.Googlemap_api import GoogleMapsAPI 
from datetime import datetime

msg = MessageManager()
app = Flask(__name__)
app.secret_key = 'abcd1234'

@app.route("/api/export/<format>", methods=["GET", "POST"])
def export_data(format):
    """
    导出数据接口
    支持格式: json, csv, xml, markdown, pdf
    """
    # 获取参数
    if request.method == "POST":
        city = request.form.get("city")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
    else:
        city = request.args.get("city")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
    
    # 调用导出管理器
    content, mimetype, extension, error = export_manager.export(
        format, city, start_date, end_date
    )
    
    if error:
        return jsonify({"status": "error", "message": error}), 400
    
    filename = f"weather_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
    
    return Response(content, mimetype=mimetype,
                   headers={"Content-Disposition": f"attachment; filename={filename}"})

@app.route("/api/export/formats", methods=["GET"])
def get_export_formats():
    """获取支持的导出格式"""
    return jsonify({
        "formats": export_manager.get_supported_formats()
    })

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

@app.route("/api/map/<city>", methods=["GET"])
def get_map(city):
    """
    Get Google Maps link for a city
    """
    result = GoogleMapsAPI.get_map_link(city)
    
    if result["status"] == "error":
        return jsonify(result), 400
    
    return jsonify(result)

@app.route("/api/map", methods=["POST"])
def get_map_post():
    """
    Get Google Maps link for a city (POST method with form data)
    
    """
    city = request.form.get("city")
    result = GoogleMapsAPI.get_map_link(city)
    
    if result["status"] == "error":
        return jsonify(result), 400
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
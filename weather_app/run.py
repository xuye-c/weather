from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/new")
def new_record():
    print("New button clicked")
    return "OK"


@app.route("/search", methods=["POST"])
def search():
    city = request.form.get("city")
    start = request.form.get("start_date")
    end = request.form.get("end_date")

    print(city, start, end)

    return f"Searching {city} from {start} to {end}"

if __name__ == '__main__':
    app.run(debug=True)
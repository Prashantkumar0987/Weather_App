import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# 🔑 Get API key from Render environment
API_KEY = os.environ.get("OPENWEATHER_API_KEY")

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")

        if not city:
            error = "Please enter a city name."
        elif not API_KEY:
            error = "API key not configured on server."
        else:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

            try:
                response = requests.get(url)
                data = response.json()

                if response.status_code != 200:
                    error = data.get("message", "City not found")
                else:
                    weather = {
                        "city": city.upper(),
                        "temp": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "wind": data["wind"]["speed"],
                        "icon": data["weather"][0]["icon"]
                    }

            except Exception as e:
                error = "Error fetching data"

    return render_template("index.html", weather=weather, error=error)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

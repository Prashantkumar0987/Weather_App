import os

try:
    from flask import Flask, render_template, request
    import requests
except ImportError:
    print("❌ Modules not installed")
    print("Run: python -m pip install flask requests")
    exit()

app = Flask(__name__)
api_key = os.environ.get("OPENWEATHER_API_KEY")

if not api_key:
    print("❌ OPENWEATHER_API_KEY is not set. You can enter the API key in the web form.")

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        form_api_key = request.form.get("api_key", "").strip()
        active_api_key = form_api_key or api_key

        if not city:
            error = "Please enter a city name."
        elif not active_api_key:
            error = "OpenWeatherMap API key is missing. Enter it in the form or set OPENWEATHER_API_KEY."
        else:
            url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?q={city}&appid={active_api_key}&units=metric"
            )
            try:
                response = requests.get(url, timeout=10)
                data = response.json()
            except requests.RequestException as exc:
                error = f"Network error: {exc}"
            else:
                if response.status_code == 401:
                    error = "Invalid API key. Please verify your OpenWeatherMap API key."
                elif response.status_code != 200:
                    error = data.get("message", "Unable to get weather data.")
                else:
                    weather = {
                        "city": city.upper(),
                        "temp": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "wind": data["wind"]["speed"],
                        "condition": data["weather"][0]["description"]
                    }
    else:
        form_api_key = ""
        city = ""

    return render_template("index.html", weather=weather, error=error, city=city, api_key=form_api_key)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
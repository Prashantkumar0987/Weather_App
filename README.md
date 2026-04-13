# Flask Weather App

A simple Flask app that fetches weather data from OpenWeatherMap.

## Setup

1. Create and activate a Python virtual environment in the project folder.
2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Set your OpenWeatherMap API key.

PowerShell:
```powershell
$env:OPENWEATHER_API_KEY='your_actual_key_here'
```

4. Run the app:

```powershell
python app.py
```

5. Open the app in your browser:

```
http://127.0.0.1:5000
```

## Notes

- Do not commit `.venv/` or any local environment files.
- If you use a different key storage method, make sure the app can access `OPENWEATHER_API_KEY`.

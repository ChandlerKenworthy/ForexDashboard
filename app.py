from flask import Flask, render_template, jsonify
import requests
from datetime import datetime, timedelta
import time

def get_forex_data(from_currency, to_currency):
    with open("api.key", "r") as f:
        API_KEY = f.read()

    # Get the current time in nanoseconds
    current_time_nanoseconds = time.time_ns()

    # Subtract 1 day from both times because I don't pay for the API
    one_day_ms = 24 * 60 * 60 * 1000

    # Convert to milliseconds
    current_time_ms = (current_time_nanoseconds // 1_000_000) - one_day_ms

    # Get that last 60 minutes of data = 60 * 60 * 1000 milliseconds
    start_time_ms = current_time_ms - (60 * 60 * 1000)

    ticker_multiplier = 1
    ticker_type = "minute"
    #yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    #today = datetime.today().strftime('%Y-%m-%d')

    url = f'https://api.polygon.io/v2/aggs/ticker/C:{from_currency}{to_currency}/range/{ticker_multiplier}/{ticker_type}/{start_time_ms}/{current_time_ms}?adjusted=true&sort=asc&apiKey={API_KEY}'

    response = requests.get(url)
    data = response.json()
    return data


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forex_data')
def forex_data():
    data = get_forex_data('EUR', 'USD')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

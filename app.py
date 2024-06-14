from flask import Flask, render_template, jsonify
import requests
from datetime import datetime, timedelta

def get_forex_data(from_currency, to_currency):
    with open("api.key", "r") as f:
        API_KEY = f.read()

    ticker_multiplier = 1
    ticker_type = "minute"
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    today = datetime.today().strftime('%Y-%m-%d')

    url = f'https://api.polygon.io/v2/aggs/ticker/C:{from_currency}{to_currency}/range/{ticker_multiplier}/{ticker_type}/{yesterday}/{today}?adjusted=true&sort=asc&apiKey={API_KEY}'

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

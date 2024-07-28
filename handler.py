from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

BOT_ID = 'your_bot_id_here'

sales_total = 0

@app.route('/callback', methods=['POST'])
def callback():
    data = request.get_json()
    process_message(data)
    return 'ok', 200

def process_message(message):
    global sales_total
    text = message['text']
    timestamp = datetime.datetime.now()

    # Check if the message is within the time range 8 AM to 4 AM
    if 8 <= timestamp.hour or timestamp.hour < 4:
        # Look for numbers following a '$' symbol in the message
        sales = extract_sales(text)
        if sales:
            sales_total += sales

def extract_sales(text):
    import re
    matches = re.findall(r'\$(\d+(?:\.\d{1,2})?)', text)
    sales_sum = sum(float(match) for match in matches)
    return sales_sum

@app.route('/sales_total', methods=['GET'])
def get_sales_total():
    return jsonify({'sales_total': sales_total})

def send_message(text):
    url = 'https://api.groupme.com/v3/bots/post'
    payload = {
        'bot_id': BOT_ID,
        'text': text
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

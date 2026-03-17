# (c)AI[Perplexity]
import os
import requests

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sendMessage', methods=['POST'])
def send_message():
    data = request.json
    bot_token = data.get('token')
    chat_id = data.get('chat_id')
    text = data.get('text')
    
    if not all([bot_token, chat_id, text]):
        return jsonify({'error': 'Missing params'}), 400
    
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    
    try:
        response = requests.post(url, json=payload)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return 'Telegram Relay OK'

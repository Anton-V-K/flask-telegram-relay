# (c)AI[Perplexity]
import requests
import subprocess

from flask import Flask, request, jsonify

app = Flask(__name__)

def get_git_hash():
    try:
        git_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], 
                                          stderr=subprocess.DEVNULL).decode().strip()
        return git_hash[:7]  # Return short hash
    except Exception:
        return 'unknown'

@app.route('/sendMessage', methods=['POST'])
def send_message():
    data = request.json
    bot_token = data.get('token')
    chat_id = data.get('chat_id')
    text = data.get('text')
    
    if not all([bot_token, chat_id, text]):
        return jsonify({'error': 'Missing params'}), 400
    
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text + ' (relay)'}
    
    try:
        response = requests.post(url, json=payload)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    git_hash = get_git_hash()
    return f'Telegram Relay OK (git: {git_hash})'

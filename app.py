# (c)AI[Perplexity+CoPilot]
import os
import requests
import subprocess

from datetime import datetime
from flask import Flask, jsonify, render_template, request, send_from_directory

app = Flask(__name__, static_folder='static', static_url_path='/static')
startup_time = datetime.now()

def get_git_hash():
    # Try Vercel environment variable first (set during deployment)
    git_hash = os.getenv('VERCEL_GIT_COMMIT_SHA')
    if git_hash:
        return git_hash[:7]  # Return short hash
    
    # Fall back to git command for local development
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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('./static', 'favicon.ico')

@app.route('/')
def home():
    git_hash = get_git_hash()
    uptime_seconds = (datetime.now() - startup_time).total_seconds()
    uptime_minutes = int(uptime_seconds // 60)
    uptime_seconds = int(uptime_seconds % 60)
    running_since = startup_time.strftime('%Y-%m-%d %H:%M:%S UTC')
    
    return render_template('index.html',
                          git_hash=git_hash,
                          running_since=running_since,
                          uptime_minutes=uptime_minutes,
                          uptime_seconds=uptime_seconds)

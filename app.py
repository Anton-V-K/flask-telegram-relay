# (c)AI[Perplexity+CoPilot]
import os
import requests
import subprocess

from datetime import datetime

from flask import Flask, request, jsonify

app = Flask(__name__)
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

@app.route('/')
def home():
    git_hash = get_git_hash()
    uptime_seconds = (datetime.now() - startup_time).total_seconds()
    uptime_minutes = int(uptime_seconds // 60)
    uptime_seconds = int(uptime_seconds % 60)
    running_since = startup_time.strftime('%Y-%m-%d %H:%M:%S UTC')
    
    html = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
                .container {{ background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 500px; }}
                .info {{ margin: 10px 0; font-size: 14px; color: #333; }}
                .label {{ font-weight: bold; color: #666; display: inline-block; width: 120px; }}
                .status {{ color: #22c55e; font-size: 24px; font-weight: bold; margin-bottom: 20px; }}
                .value {{ color: #22c55e; font-family: monospace; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="status">✓ Telegram Relay OK</div>
                <div class="info">
                    <span class="label">Git Hash:</span>
                    <span class="value">{git_hash}</span>
                </div>
                <div class="info">
                    <span class="label">Running Since:</span>
                    <span class="value">{running_since}</span>
                </div>
                <div class="info">
                    <span class="label">Uptime:</span>
                    <span class="value">{uptime_minutes}m {uptime_seconds}s</span>
                </div>
            </div>
        </body>
    </html>
    """
    return html

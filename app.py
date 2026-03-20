# (c)AI[Perplexity+CoPilot]
from datetime import datetime
from flask import Flask, jsonify, render_template, request, send_from_directory

from core import get_git_hash, get_git_message, send_telegram_message

app = Flask(__name__, static_folder='static', static_url_path='/static')
startup_time = datetime.now()

@app.route('/sendMessage', methods=['POST'])
def send_message():
    # Support multiple content types: JSON, form data, and URL-encoded
    if request.is_json:
        data = request.json
    else:
        data = request.form.to_dict()
    
    bot_token = data.get('token')
    chat_id = data.get('chat_id')
    text = data.get('text')
    
    if not all([bot_token, chat_id, text]):
        return jsonify({'error': 'Missing params'}), 400
    
    try:
        response = send_telegram_message(bot_token, chat_id, text)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bot/<bot_token>/sendMessage', methods=['POST'])
def send_message_with_token(bot_token):
    # Support multiple content types: JSON, form data, and URL-encoded
    if request.is_json:
        data = request.json
    else:
        data = request.form.to_dict()
    
    chat_id = data.get('chat_id')
    text = data.get('text')
    
    if not all([chat_id, text]):
        return jsonify({'error': 'Missing params'}), 400
    
    try:
        response = send_telegram_message(bot_token, chat_id, text)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('./static', 'favicon.ico')

@app.route('/')
def home():
    git_hash = get_git_hash()
    git_message = get_git_message()
    uptime_seconds = (datetime.now() - startup_time).total_seconds()
    uptime_minutes = int(uptime_seconds // 60)
    uptime_seconds = int(uptime_seconds % 60)
    running_since = startup_time.strftime('%Y-%m-%d %H:%M:%S UTC')
    
    return render_template('index.html',
                          git_hash=git_hash,
                          git_message=git_message,
                          running_since=running_since,
                          uptime_minutes=uptime_minutes,
                          uptime_seconds=uptime_seconds)

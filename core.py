"""
(c)AI[CoPilot]
Core Telegram relay functionality that can be used independently of Flask.
"""
import os
import requests
import subprocess


def get_git_hash():
    """
    Get the current git commit hash (short form).
    
    Returns:
        str: Short git hash (7 characters), or 'unknown' if not available.
    """
    # Try Vercel environment variable first
    # Refer to https://vercel.com/docs/environment-variables/system-environment-variables
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


def get_git_message():
    """
    Get the current git commit message.
    
    Returns:
        str: Commit message (first line), or 'unknown' if not available.
    """
    # Try Vercel environment variable first
    # Refer to https://vercel.com/docs/environment-variables/system-environment-variables
    message = os.getenv('VERCEL_GIT_COMMIT_MESSAGE')
    if message:
        return message.split('\n')[0]  # Return first line only
    
    # Fall back to git command for local development
    try:
        message = subprocess.check_output(['git', 'log', '-1', '--format=%B'], 
                                         stderr=subprocess.DEVNULL).decode().strip()
        return message.split('\n')[0] if message else 'unknown'  # Return first line only
    except Exception:
        return 'unknown'


def send_telegram_message(bot_token, chat_id, text):
    """
    Send a message to a Telegram chat using the Telegram Bot API.
    
    Args:
        bot_token (str): Telegram bot token
        chat_id (str): Telegram chat ID
        text (str): Message text to send
        
    Returns:
        dict: Response from Telegram API
        
    Raises:
        requests.RequestException: If the API request fails
    """
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text + ' (relay)'}
    
    response = requests.post(url, json=payload)
    return response.json()

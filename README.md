# flask-telegram-relay

A simple Flask application that relays messages to Telegram via the Telegram Bot API. Perfect for integrating Telegram notifications into your applications.

## Features

- Send messages to Telegram through a simple HTTP POST endpoint
- Health check endpoint
- Lightweight and easy to deploy
- Pre-configured for Vercel deployment

## Installation

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd flask-telegram-relay
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

   The server will start at `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/`
- Returns: `Telegram Relay OK`

### Send Message to Telegram
- **POST** `/sendMessage`
- **Content-Type:** `application/json`
- **Parameters:**
  - `token` (string): Your Telegram Bot API token
  - `chat_id` (string/int): The Telegram chat ID to send the message to
  - `text` (string): The message text to send

**Example Request:**
```bash
curl -X POST http://localhost:5000/sendMessage \
  -H "Content-Type: application/json" \
  -d '{
    "token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID",
    "text": "Hello from flask-telegram-relay!"
  }'
```

**Example Response:**
```json
{
  "ok": true,
  "result": {
    "message_id": 123,
    "date": 1626234567,
    "chat": {"id": 12345},
    "text": "Hello from flask-telegram-relay!"
  }
}
```

## Deployment to Vercel

### Prerequisites
- Vercel account (free at https://vercel.com)
- Git repository (GitHub, GitLab, or Bitbucket)

### Deploy via Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

3. **Follow the prompts** and your app will be deployed!

### Deploy via GitHub

1. **Push your repository to GitHub**

2. **Connect to Vercel:**
   - Go to https://vercel.com/new
   - Select your GitHub repository
   - Click "Import"
   - Vercel will auto-detect the configuration from `vercel.json`
   - Click "Deploy"

3. **Your app is live!** You'll get a URL like `https://your-project.vercel.app`

## Usage

Once deployed, use your Vercel URL to send messages:

```bash
curl -X POST https://your-project.vercel.app/sendMessage \
  -H "Content-Type: application/json" \
  -d '{
    "token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID",
    "text": "Message from Vercel!"
  }'
```

## Getting Your Telegram Bot Token and Chat ID

### Bot Token
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Use `/newbot` command and follow instructions
3. Copy your bot token (looks like `123456789:ABCDefGHijKlMNOpQRstUVwxyz`)

### Chat ID
1. Message your bot with any text
2. Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Look for `message.chat.id` in the response

## Environment Variables

While this app works with tokens passed in the request body, for production consider storing sensitive tokens as environment variables in Vercel:

1. Go to your Vercel project settings
2. Navigate to "Environment Variables"
3. Add your secrets
4. Update the application code to use `os.getenv('TELEGRAM_BOT_TOKEN')` etc.

## License

See LICENSE file for details.

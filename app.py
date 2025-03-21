from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime, time

app = Flask(__name__)

# Replace with your actual Telegram public channel URL
CHANNEL_URL = "https://t.me/s/YOUR_CHANNEL_USERNAME"  # <-- EDIT THIS

def get_latest_telegram_message():
    response = requests.get(CHANNEL_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Telegram message containers
    posts = soup.find_all("div", class_="tgme_widget_message_wrap")

    # Define the target time: 8:30 AM today
    target_time = datetime.combine(datetime.today(), time(8, 30))

    for post in posts:
        # Get message text
        msg_text_div = post.find("div", class_="tgme_widget_message_text")
        if not msg_text_div:
            continue
        msg_text = msg_text_div.get_text().strip()

        # Get message time (from <time datetime="...">)
        time_tag = post.find("time")
        if not time_tag or not time_tag.has_attr("datetime"):
            continue

        post_time_str = time_tag["datetime"]  # ISO format e.g., 2025-03-21T08:32:00+00:00
        post_time = datetime.fromisoformat(post_time_str.replace("Z", "+00:00")).astimezone()

        if post_time >= target_time:
            return msg_text

    return "No message found after 8:30 AM today."

@app.route("/")
def home():
    return "✅ Telegram Daily Scraper is running!"

@app.route("/daily", methods=["GET"])
def daily_message():
    message = get_latest_telegram_message()
    today = datetime.now().strftime("%Y-%m-%d")
    return jsonify({
        "date": today,
        "message": message
    })

if __name__ == "__main__":
    app.run()

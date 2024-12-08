# import logging
# logging.basicConfig(level=logging.DEBUG)

import os
import json
from utils.time import convert_to_kst
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.selenium.scraper import ChatGPTScraper

SLACK_BOT_TOKEN = "YOUR_BOT_TOKEN"

client = WebClient(token=SLACK_BOT_TOKEN)


def slack_event_handler(event_data: dict, scraper: ChatGPTScraper, database: dict):
    event = event_data.get("event", {})

    if event.get("type") == "message" and "bot_id" not in event:  # Ignore bot messages
        channel_id = event.get("channel")
        ts = event.get("ts")
        thread_ts = event.get("thread_ts", ts)
        info_message = (
            f"no matching thread: {database.get(thread_ts, None)}"
            if thread_ts != ts
            else f"matching thread: {database.get(thread_ts, None)}"
        )
        print(f"# [INFO] Received message: {info_message}")

        # current_time = convert_to_kst(ts) # debug
        current_text = event.get("text")
        current_url = database.get(thread_ts, None)
        response_text, current_url = scraper.search_chatgpt(current_url, current_text)

        update_database(database, thread_ts, current_url)
        send_thread_message(channel_id, thread_ts, f"{response_text}")


def send_thread_message(channel_id: str, thread_ts: str, text: str):
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            thread_ts=thread_ts,
            text=text,
        )
        return response
    except SlackApiError as e:
        return {"error": str(e)}


def read_database():
    print("# [INFO] Reading database")
    if not os.path.exists("database.json"):
        with open("database.json", "w") as f:
            json.dump({}, f)
    with open("database.json", "r") as f:
        database = json.load(f)
    print("# [INFO] Database loaded")
    return database


def update_database(database, key, value):
    if key in database and database[key] == value:
        return
    database[key] = value
    print(f"# [INFO] Updated database: {key}={value}")
    write_database(database)


def write_database(database):
    print("# [INFO] Writing database")
    with open("database.json", "w") as f:
        json.dump(database, f)
    print("# [INFO] Database saved")

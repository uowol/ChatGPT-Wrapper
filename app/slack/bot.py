# import logging
# logging.basicConfig(level=logging.DEBUG)

import os
from utils.time import convert_to_kst
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.selenium.scraper import ChatGPTScraper

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

client = WebClient(token=SLACK_BOT_TOKEN)


def slack_event_handler(event_data: dict, scraper: ChatGPTScraper):
    event = event_data.get("event", {})

    if event.get("type") == "message" and "bot_id" not in event:  # Ignore bot messages
        channel_id = event.get("channel")
        thread_ts = event.get("ts")

        current_time = convert_to_kst(thread_ts)
        current_text = event.get("text")
        response_text = scraper.search_chatgpt(current_text)
        send_thread_message(
            channel_id, thread_ts, response_text
        )  # TODO: 새 쓰레드에서 채팅하는 경우 chatgpt 또한 새 채팅을 시작하기


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

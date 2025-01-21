import os
import json
import time
from fastapi import FastAPI, Request
from pydantic import BaseModel

from app.slack.bot import slack_event_handler, read_database
from app.selenium.scraper import ChatGPTScraper


CHROME_SUBPROCESS_PATH = os.getenv(
    "CHROME_SUBPROCESS_PATH",
    r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"',
)
SUBPROCESS_PORT = os.getenv("SUBPROCESS_PORT", 9222)


app = FastAPI()
database = read_database()  # load database from filesystem(AS-IS: local, TO-BE: s3)
scraper = ChatGPTScraper(
    subprocess_path=CHROME_SUBPROCESS_PATH, subprocess_port=SUBPROCESS_PORT
)  # run scraper(selenium) with subprocess


# Control slack events
@app.post("/slack/events")
async def slack_events(request: Request):
    headers = request.headers
    if headers.get("X-Slack-Retry-Num"):
        return {"status": "ok"}

    event_data = await request.json()
    if "challenge" in event_data:
        return {"challenge": event_data["challenge"]}

    response = slack_event_handler(event_data, scraper, database)
    return {"status": "ok"} if response else {"status": "error"}


# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}


class Response(BaseModel):
    response: str
    url: str
    details: dict  # endpoint, status, model


# API reference
@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    data = await request.json()
    model = data.get("model")
    messages = data.get("messages")
    text = ""

    for msg in messages:
        role = msg.get("role")
        content = msg.get("content")
        if role in ["system", "developer"]:
            text += f"[SYSTEM] This is a system-specific response. {content} "
        else:
            text += f"[USER] {content} "

    try:
        url = scraper.url + f"?model={model}"
        response_text, current_url = scraper.search_chatgpt(url, text)
    except Exception as e:
        response_text = f"Error during ChatGPT completions: {e}"
        current_url = None

    return Response(
        response=response_text,
        url=current_url,
        details={"endpoint": "/v1/chat/completions", "status": "ok", "model": model},
    ).model_dump_json()

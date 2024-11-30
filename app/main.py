from fastapi import FastAPI, Request
from app.slack_handler import handle_slack_event
from utils.time import convert_to_kst

app = FastAPI()


@app.post("/slack/events")
async def slack_events(request: Request):
    event_data = await request.json()

    if (
        "challenge" in event_data
    ):  # Slack sends a challenge event when the server is first connected
        return {"challenge": event_data["challenge"]}

    handle_slack_event(event_data)
    return {"message": "Event received"}

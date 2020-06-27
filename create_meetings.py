import requests
import json


def create_meetings(uuid, jwt, data):
    url = "https://api.zoom.us/v2/users/{}/meetings"
    url = url.format(uuid)
    payload = {
        "type": data["meeting_type"],
        "duration": data["duration"],
        "start_time": data["start_time"],
        "topic": data["topic"],
        "timezone": "America/New_York",
        "settings": {
            "join_before_host": True,
            "host_video": True,
            "approval_type": 0,
            "registration_type": 1,
            "registrants_email_notification": True
        }
    }
    if data["meeting_type"] == 3 or data["meeting_type"] == 8:
        payload["recurrence"] = {
            "type": data["recurrence_type"],
            "repeat_interval": data["repeat_interval"],
            "end_times": data["end_times"]
        }

    headers = {
        'Accept': "application/json, application/xml",
        'Content-Type': "application/json",
        'Authorization': jwt
    }
    response = requests.post(
        url,
        data=json.dumps(payload),
        headers=headers
    )
    response = response.json()
    response["statusCode"] = 200
    return response
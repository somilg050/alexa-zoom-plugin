import requests
import json


def change_meeting_status(token, action, meetingObj):
    if action == "start":
        try:
            r = requests.get(meetingObj["join_url"])
        except:
            print(r.status_code)
        finally:
            return {
                "statusCode": 200,
                "message": "Meeting has started. Please join on link"+ meetingObj["join_url"]
            }
    else:
        url = "https://api.zoom.us/v2/meetings/{}/status"
        url = url.format(meetingObj["id"])
        payload = json.dumps({"action": "end"})
        headers = {
            'Content-Type': "application/json",
            'Authorization': token
        }
        requests.put(url, data=payload, headers=headers)
        return {
            "statusCode": 200,
            "message": "Meeting Ended Succesfully"
        }
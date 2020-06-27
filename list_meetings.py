import requests
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
from time import sleep


def list_meetings(pageno=1, userid="foo@bar.com", jwt=""):
    url = "https://api.zoom.us/v2/users/{}/meetings"
    url = url.format(userid)
    querystring = {
        "type":"upcoming",
        "page_size":"100",
        "page_number":str(pageno)
    }
    headers = {
        'Accept': "application/json, application/xml",
        'Content-Type': "application/json",
        'Authorization': jwt
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    today_s_meetings = []
    for i in data["meetings"]:
        if i["type"] == 3:
            current_time = datetime.now(timezone.utc)
            meeting_time = parse(i["start_time"])
            next_day = current_time+timedelta(hours=24)
            if meeting_time >= current_time and meeting_time <= next_day:
                today_s_meetings.append(i)
        else:
            today_s_meetings.append(i)
    for i in today_s_meetings:
        i["registrants"] = list_registrants(i["id"], i["uuid"], jwt)
        sleep(1)
    data["meetings"] = today_s_meetings
    data["statusCode"] = response.status_code
    return data


def list_registrants(meeting_id, uuid, token):
    url = "https://api.zoom.us/v2/meetings/{}/registrants"
    url = url.format(meeting_id)
    querystring = {
        "occurrence_id":uuid,
        "status":"approved",
        "page_size":"30",
        "page_number":"1"
    }
    headers = {
        'Accept': "application/json, application/xml",
        'Content-Type': "application/json",
        'Authorization': token
    }
    response = requests.get(url, headers=headers, params=querystring)
    try:
        return response.json()["registrants"]
    except:
        return response.json()
    
import json

import requests

def all_downloader(video_url:str):

    url = "https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink"

    payload = {"url": video_url}
    headers = {
        "x-rapidapi-key": "846d3ddb53mshf1921d1525a24e2p1581c9jsn138d58bd50c9",
        "x-rapidapi-host": "social-download-all-in-one.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    res = json.loads(response.text)

    if res.get('error'):
        return False

    return res.get('medias')[0].get('url')

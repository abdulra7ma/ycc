import urllib3
import json
import requests
import re


def get_all_video_in_channel(channel_id):
    api_key = "AIzaSyAJlHSK1Is_xrDSHVG220RYCQVT_BgkbK0"

    base_video_url = "https://www.youtube.com/watch?v="
    base_search_url = "https://www.googleapis.com/youtube/v3/search?"

    first_url = (
        base_search_url
        + "key={}&channelId={}&part=snippet,id&order=date&maxResults=25".format(
            api_key, channel_id
        )
    )

    video_links = []
    url = first_url
    while True:
        inp = requests.get(url)
        resp = json.loads(inp.content)

        print(resp.keys())
        print(resp["error"])

        for i in resp["items"]:
            if i["id"]["kind"] == "youtube#video":
                video_links.append(base_video_url + i["id"]["videoId"])

        try:
            next_page_token = resp["nextPageToken"]
            url = first_url + "&pageToken={}".format(next_page_token)
        except:
            break
    return video_links


# return YouTube channel id via handle or False if failed
def scraping_get_channel_id_from_handle(handle: str):
    if handle.find("@") == -1:
        handle = "@" + handle

    url = "https://www.youtube.com/" + handle
    resp = requests.get(url)

    if resp.status_code == 200:
        found = re.findall('"channelId":"([^"]*)","title"', resp.text)
        return found[0]
    else:
        return False

import os
import csv
import re
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from utils import extract_handle
from youtube_video import (
    get_all_video_in_channel,
    scraping_get_channel_id_from_handle,
)
import scrapetube


class YoutubeVideo:
    def __init__(self, api_key=None, credentials_file=None):
        self.api_key = api_key
        self.credentials_file = credentials_file
        self.comments = []
        self.likes = None

    def __str__(self):
        return (
            f" Likes: {self.likes}, Number of Comments: {len(self.comments)}"
        )

    def get_youtube_service(self):
        if self.credentials_file is not None:
            credentials = (
                service_account.Credentials.from_service_account_file(
                    self.credentials_file,
                    scopes=[
                        "https://www.googleapis.com/auth/youtube.force-ssl"
                    ],
                )
            )
        else:
            credentials = None

        youtube = build(
            "youtube", "v3", credentials=credentials, developerKey=self.api_key
        )
        return youtube

    def get_video_info(self, video_id):
        youtube = self.get_youtube_service()

        try:
            video_response = (
                youtube.videos().list(part="statistics", id=video_id).execute()
            )
            video_info = video_response["items"][0]["statistics"]
            self.likes = int(video_info["likeCount"])

        except HttpError as error:
            print(f"An error occurred: {error}")
            self.likes = None

    def get_comments(self, video_id):
        youtube = self.get_youtube_service()

        next_page_token = ""
        while True:
            try:
                comment_response = (
                    youtube.commentThreads()
                    .list(
                        part="snippet",
                        videoId=video_id,
                        pageToken=next_page_token,
                        textFormat="plainText",
                    )
                    .execute()
                )
                for comment_thread in comment_response["items"]:
                    comment = comment_thread["snippet"]["topLevelComment"][
                        "snippet"
                    ]
                    self.comments.append(
                        {
                            # "comment_id": comment["commentId"],
                            "author": comment["authorDisplayName"],
                            "text": comment["textDisplay"],
                            "likes": comment["likeCount"],
                            "published_at": comment["publishedAt"],
                            "video_id": video_id,
                        }
                    )

                if "nextPageToken" in comment_response:
                    next_page_token = comment_response["nextPageToken"]
                else:
                    break
            except HttpError as error:
                print(f"An error occurred: {error}")
                break

    def get_video_id_from_url(self, url):
        """
        Given a URL, return the video ID.
        Ex: https://www.youtube.com/watch?v=E4QwKj_SthY
        returns: E4QwKj_SthY
        """
        return re.search(r"watch\?v=(.{11})", url, re.IGNORECASE).group(1)

    def download_comments_to_csv(self, file_name):
        with open(file_name, "a", newline="", encoding="utf-8") as csv_file:
            fieldnames = [
                "author",
                "text",
                "likes",
                "published_at",
                "video_id",
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if not os.path.exists(os.path.dirname(file_name)):
                writer.writeheader()
            for comment in self.comments:
                writer.writerow(comment)
        print(f"Successfully saved comments to {os.path.abspath(file_name)}")


if __name__ == "__main__":
    # Replace with your YouTube API key
    api_key = "AIzaSyAJlHSK1Is_xrDSHVG220RYCQVT_BgkbK0"

    # Create an instance of the YouTubeVideo class
    

    youtube_channels = [
        # "https://www.youtube.com/@Media-qy6oc/videos",
        # "https://www.youtube.com/@bairakgroup/videos",
        # "https://www.youtube.com/@user-rg4yt3uz1i/videos",
        # "https://www.youtube.com/@nsns466/videos",
        "https://www.youtube.com/@SUPERTV_TELEKANAL/videos",
        "https://www.youtube.com/@AzattykMedia/videos",
        "https://www.youtube.com/@temirovlivekg4060/videos",
        "https://www.youtube.com/@tezkabar1/videos",
        "https://www.youtube.com/@newtv6071/videos",
        "https://www.youtube.com/@NewTV2/videos",
        "https://www.youtube.com/@SanjarKalmataiKyrgyzKabarlar/videos",
        "https://www.youtube.com/@salammedia106.40/videos",
        "https://www.youtube.com/@AlaToo24UTRK/videos",
        "https://www.youtube.com/@KTRKkgchannel/videos/",
        "https://www.youtube.com/@NewTVShowKG/videos",
        "https://www.youtube.com/@NewBroadcastingNet/videos",
        "https://www.youtube.com/@tvkaiguul3542/videos",
        "https://www.youtube.com/@Amanat_media/videos",
        "https://www.youtube.com/@kyrgyztop/videos",
        "https://www.youtube.com/@naziraaytbekova./videos",
        "https://www.youtube.com/@aalamkabar6061/videos",
        "https://www.youtube.com/@radiomaral/videos",
    ]

    for channel in youtube_channels:
        handle = extract_handle(channel)

        # print(channel.get_videos())
        channel_id = scraping_get_channel_id_from_handle(handle)

        videos = scrapetube.get_channel(channel_id)
        count = 0

        Video = YoutubeVideo(api_key)

        video_list = []

        for video in videos:
            Video.get_comments(video["videoId"])

        Video.download_comments_to_csv(f"comments/{handle}.csv")

    # Get the comments and save them to a CSV file
    # comment_list = video.download_comments_to_csv("comments.csv")

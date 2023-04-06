from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import csv
import os

class YouTubeVideo:
    def __init__(self, video_id, api_key, credentials_file="credentials.json"):
        self.video_id = video_id
        self.api_key = api_key

        # Load the credentials from the JSON file
        creds = None
        if os.path.exists(credentials_file):
            creds = Credentials.from_authorized_user_file(credentials_file, scopes=["https://www.googleapis.com/auth/youtube.force-ssl"])
        else:
            print(f"Credentials file '{credentials_file}' not found. Proceeding with API key authentication.")

        # Build the API client with the credentials or API key
        if creds is not None:
            self.youtube = build("youtube", "v3", credentials=creds)
        else:
            self.youtube = build("youtube", "v3", developerKey=self.api_key)
        
        # Get the video details
        video_response = self.youtube.videos().list(
            part="snippet,statistics",
            id=self.video_id,
            key=self.api_key
        ).execute()

        # Get the likes and dislikes of the video
        self.likes = video_response['items'][0]['statistics']['likeCount']
        print(f"Likes: {self.likes}")
        # self.dislikes = video_response['items'][0]['statistics']['dislikeCount']

    def get_comments(self):
        # Get the comments for the video
        comments_response = self.youtube.commentThreads().list(
            part="snippet",
            videoId=self.video_id,
            key=self.api_key
        ).execute()

        # Create a list to store the comments and their likes and replies
        comment_list = []
        for comment in comments_response['items']:
            comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
            comment_likes = comment['snippet']['topLevelComment']['snippet']['likeCount']
            comment_replies = comment['snippet']['totalReplyCount']
            comment_list.append([comment_text, comment_likes, comment_replies])

        # Save the data to a CSV file
        with open('video_comments.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Comment', 'Likes', 'Replies'])
            for comment in comment_list:
                writer.writerow(comment)

        return comment_list

    def print_likes_and_dislikes(self):
        print(f"Likes: {self.likes}")

if __name__ == '__main__':
    # Replace with your YouTube API key
    api_key = "AIzaSyAJlHSK1Is_xrDSHVG220RYCQVT_BgkbK0"

    # Video ID of the YouTube video
    video_id = "E4QwKj_SthY"

    # Create an instance of the YouTubeVideo class
    video = YouTubeVideo(video_id, api_key)

    # Get the comments and save them to a CSV file
    comment_list = video.get_comments()

    # Print the likes and dislikes of the video
    video.print_likes_and_dislikes()

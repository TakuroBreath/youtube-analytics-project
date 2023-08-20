import os
from googleapiclient.discovery import build

API_KEY = os.getenv('API_KEY')


class Video:

    def __init__(self, video_id):
        api_key: str = API_KEY
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        self.video_id = video_id
        self.name = video_response['items'][0]['snippet']['title']
        self.video_url = f"https://www.youtube.com/watch?v={video_id}"
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.name

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=API_KEY)


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

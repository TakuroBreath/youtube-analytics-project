import json
import os
from googleapiclient.discovery import build
import isodate


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

    @property
    def channel_id(self):
        return self.__channel_id

    def __str__(self):
        api_key: str = os.getenv("API_KEY")
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.subscribers) + int(other.subscribers)

    def __sub__(self, other):
        return int(self.subscribers) - int(other.subscribers)

    def __lt__(self, other):
        return int(self.subscribers) < int(other.subscribers)

    def __le__(self, other):
        return int(self.subscribers) <= int(other.subscribers)

    def __gt__(self, other):
        return int(self.subscribers) > int(other.subscribers)

    def __ge__(self, other):
        return int(self.subscribers) >= int(other.subscribers)

    def __eq__(self, other):
        return int(self.subscribers) == int(other.subscribers)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key: str = os.getenv("API_KEY")
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @property
    def title(self):
        api_key: str = os.getenv("API_KEY")
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return channel['items'][0]['snippet']['title']

    @property
    def video_count(self):
        api_key: str = os.getenv("API_KEY")
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='statistics').execute()
        return channel['items'][0]['statistics']['videoCount']

    @property
    def url(self):
        return f"https://www.youtube.com/channel/{self.channel_id}"

    @property
    def description(self):
        api_key: str = os.getenv("API_KEY")
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return channel['items'][0]['snippet']['description']

    @property
    def subscribers(self):
        api_key: str = os.getenv("API_KEY")
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='statistics').execute()
        return channel['items'][0]['statistics']['subscriberCount']

    @property
    def views(self):
        api_key: str = os.getenv("API_KEY")
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='statistics').execute()
        return channel['items'][0]['statistics']['viewCount']

    @staticmethod
    def get_service():
        api_key: str = os.getenv("API_KEY")
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, filename):
        api_key: str = os.getenv("API_KEY")
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        with open(filename, "w") as f:
            json.dump(channel, f)

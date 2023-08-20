from datetime import timedelta

import isodate

from src.video import PLVideo, Video


class PlayList(Video):
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlist = super().get_service().playlists().list(id=playlist_id, part="id, snippet").execute()
        self.title = playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlist['items'][0]['id']}"

        playlist_videos = super().get_service().playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        self.video_response = super().get_service().videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
    def __str__(self):
        return self.title

    @property
    def playlist_id(self):
        return self.playlist_id

    @playlist_id.setter
    def playlist_id(self, value):
        self.__playlist_id = value

    @property
    def total_duration(self):
        total_duration = 0

        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration).seconds
            total_duration += duration

        return timedelta(seconds=total_duration)

    def show_best_video(self):
        max_likes = 0
        best_video = ""

        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > max_likes:
                max_likes = int(video['statistics']['likeCount'])
                best_video = video['id']

        return f"https://youto.be/{best_video}"

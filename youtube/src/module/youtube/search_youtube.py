# module/youtube/search_youtube.py
import requests

def search_youtube(search_query, api_key):
    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': search_query,
        'type': 'video',
        'maxResults': 1,
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json()['items']
        if results:
            video_id = results[0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return video_url
        else:
            return "No results found."
    else:
        return "Failed to retrieve results."

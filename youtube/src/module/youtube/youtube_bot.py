import irc.bot
import re
import requests
import isodate
import threading
import time

class YouTubeBot(irc.bot.SingleServerIRCBot):
    def __init__(self, server, port, channel, bot_name, api_key=None):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], bot_name, bot_name)
        self.channels = {}
        self.api_key = api_key
        self.youtube_pattern = r"(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})"
        self.ping_thread = threading.Thread(target=self.ping_server, daemon=True)
        self.ping_thread.start()

    def ping_server(self):
        while True:
            if self.connection.is_connected():
                self.send_ping()
            time.sleep(200)  # Send PING 

    def send_ping(self):
        self.connection.ping("ping")
        
    def on_pong(self, connection, event):
        print("Received PONG response from server.")

    def on_welcome(self, connection, event):
        connection.join(channel)
        self.channels[channel] = {}

    def on_pubmsg(self, connection, event):
        msg = event.arguments[0]
        youtube_links = re.findall(self.youtube_pattern, msg)
        if youtube_links:
            self.process_youtube_links(connection, youtube_links, event.target)

    def process_youtube_links(self, connection, youtube_links, target_channel):
        for video_id in youtube_links:
            response = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={video_id}&key={self.api_key}")
            if response.status_code == 200:
                video_info = response.json()
                if "items" in video_info and video_info["items"]:
                    snippet = video_info["items"][0]["snippet"]
                    statistics = video_info["items"][0]["statistics"]
                    content_details = video_info["items"][0]["contentDetails"]
                    title = snippet["title"]
                    duration_iso = content_details.get("duration", "PT0S")
                    duration_human = isodate.parse_duration(duration_iso)
                    minutes, seconds = divmod(duration_human.total_seconds(), 60)
                    duration_str = f"{int(minutes)}m{int(seconds)}s"
                    views = statistics.get("viewCount", "N/A")
                    output_message = f"\x02\x0301,00You\x0F\x02\x0300,04Tube\x0F {title} - Duration: {duration_str} - Views: {views}"
                    connection.privmsg(target_channel, output_message)
            else:
                print("Error fetching video information.")


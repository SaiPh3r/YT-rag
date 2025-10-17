from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()
video_id = "uOcKF-aLHyw" 

try:
        transcript = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
        for snippet in transcript:
            print(f"{snippet.start}: {snippet.text} ({snippet.duration})")


except Exception as e:
        print("Failed to fetch transcript:", str(e))





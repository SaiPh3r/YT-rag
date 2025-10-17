from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

load_dotenv()
video_id = "uOcKF-aLHyw" 

try:
        transcript = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
        for snippet in transcript:
            print(f"{snippet.start}: {snippet.text} ({snippet.duration})")

except NoTranscriptFound:
        print("No captions found for video:", video_id)
except Exception as e:
        print("Failed to fetch transcript:", str(e))





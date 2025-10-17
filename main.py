from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()
# code to get transcript from youtube 
video_id = "uOcKF-aLHyw" 

try:
        transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
        transcript = ""
        for snippet in transcript_list:
                transcript += snippet.text+" "
        # print(transcript)

except Exception as e:
        print("Failed to fetch transcript:", str(e))

#  text splitting and chunking of the transcript
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = splitter.create_documents([transcript])
# print(texts[0].page_content)







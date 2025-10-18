from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()
# code to get transcript from youtube 
video_id = "c5BIA5RpSpo" 
transcript = ""

try:
        transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
        for snippet in transcript_list:
                transcript += snippet.text+" "
        # print(transcript)

except Exception as e:
        print("Failed to fetch transcript:", str(e))

#  text splitting and chunking of the transcript
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = splitter.create_documents([transcript]) # texts are chunks of the transcript
# print(texts[0].page_content)

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vector_db  = FAISS.from_documents(texts, embeddings)
# print(vector_db.index_to_docstore_id)   # to see the index of the vector db










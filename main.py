from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings , ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_core.output_parsers import StrOutputParser

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
# print(len(texts))

retrieval = vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 2})

result = retrieval.invoke('What does “CRUD” stand for ?')
# print(result)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt = PromptTemplate(
        template="""
        You are a helpful assistant that answers questions about youtube videos.
        You are given the following extracted parts of a long document and a question. Provide a conversational answer based on the context provided.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        {context} 
        Question: {question}
        """,

        input_variables=["context", "question"]
)

question = "How can I become a better developer?"
retriverDocs = retrieval.invoke(question)
# print(retriverDocs)

content_text = ""
for doc in retriverDocs:
        content_text += doc.page_content

# print(content_text)

# final_prompt = prompt.format(context = content_text , question = question)
# # print(final_prompt)

# answer = llm.invoke(final_prompt)
# print(answer)

def format_doc(retriverDocs):
        content_text = ""
        for doc in retriverDocs:
                content_text += doc.page_content
        return content_text

parallel_chain = RunnableParallel({
        'context' : retrieval | RunnableLambda(format_doc) , 
        'question': RunnablePassthrough()
} 
)
# print(parallel_chain.invoke("what is crud"))

parser = StrOutputParser()
final_chain = parallel_chain | prompt | llm | parser
result = final_chain.invoke("what is crud")
print(result)


 
















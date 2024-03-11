import streamlit as st
from dotenv import load_dotenv
from RAG import RAG
from google.cloud import aiplatform
from langchain_openai import OpenAIEmbeddings
import os

st.set_page_config(layout="wide")
load_dotenv()

# aiplatform.init(
#     project = os.environ.get("PROJECT_ID"),
#     location = "europe-west1"
# )

@st.cache_resource
def get_embedding_model():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large",dimensions=256)
    return embeddings

def load_rag(_chat_box):
    embeddings = get_embedding_model()
    rag = RAG(_chat_box,embeddings)
    return rag

def display_source_documents(source_documents):
    for document,score in source_documents:
        metadata = document['metadata']
        page_content = document['page_content']

        id = metadata['id']
        title = metadata['title']
        url_pdf = metadata['url_pdf']
        arxiv_id = metadata['arxiv_id']
        authors = metadata['authors']
        published = metadata['published']


        with st.container(border = True):
            st.markdown(f"Title: {title}, score = {score}")
            st.markdown(f"arxiv id: {arxiv_id}")
            st.markdown(f"authors: {','.join(authors)}")
            st.markdown(f"Publication date: {published}")
            st.markdown(f"URL: {url_pdf}")
            st.write("Context: {document_content}")


input_question = st.text_input("Ask your question here...")
columns = st.columns(2) 

with columns[0]:
    chat_box = st.empty()

rag = load_rag(chat_box)

if(input_question.strip != ""):
    with st.spinner("Generating answer.."):
        prediction = rag.predict(input_question)
    
    answer = prediction['answer']
    source_documents = prediction['source_documents']

    with columns[1]:
        st.write("Source documents: ")
        display_source_documents(source_documents)
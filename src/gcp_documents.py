import requests
from bs4 import BeautifulSoup
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import VertexAIEmbeddings
import pandas as pd
import json
from src.gcs_service import GCSService

embeddings = VertexAIEmbeddings()

def parse_generic_sitemap(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")
    urls = [element.text for element in soup.find_all("loc")]
    return urls

def filter_sites(sites):
    return [url for url in sites if '/reference/' not in url and '?hl' not in url]

def load_urls(urls):
    loader = UnstructuredURLLoader(urls=urls, mode="single", show_progress_bar=False, ssl_verify=False)
    return loader.load()

def chunk_documents(documents):
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap  = 100
    )

    document_chunks = text_splitter.split_documents(documents)
    return [f"Context: {chunk.page_content} Source: {chunk.metadata['source']}" for chunk in document_chunks]

def create_embeddings(product: str, document_chunks, gcs_service: GCSService):
    df = pd.DataFrame(document_chunks, columns =['text'])
    index_embeddings = ''
    
    for index, doc in df.iterrows():
        embedding = embeddings.embed_query(doc['text'])
        if embedding is not None:
            doc_id=f"{product}-{index}.txt"
            embedding_dict = {
                "id": doc_id,
                "embedding": [str(value) for value in embedding],
            }
            index_embeddings += json.dumps(embedding_dict) + "\n"
            gcs_service.create_document(doc_id, doc['text'])
    
    gcs_service.create_embedding(product, index_embeddings)
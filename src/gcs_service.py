from fastapi import HTTPException
from google.cloud import storage
from src.logger import logger

PUBLIC_WEBSITES_PATH = "public_websites"
DOCUMENTS_PATH = "documents"
EMBEDDINGS_PATH = "embeddings"

class GCSService:

    def __init__(self, bucket_name: str):
        self.client: storage.Client = storage.Client()
        self.bucket: storage.Bucket = self.client.bucket(bucket_name)
        self.bucket_name: str = bucket_name
        self.new_bucket = not self.bucket.exists()
        if self.new_bucket:
            try:
                self.bucket.create()
            except Exception as e:
                logger.log_text(f"Error creating bucket {bucket_name}", e)
                raise HTTPException(status_code=400, detail="Invalid bucket name")

    def create_document(self, file_name: str, content: str):
        self.create(f"{PUBLIC_WEBSITES_PATH}/{DOCUMENTS_PATH}/{file_name}", content)
    
    def create_embedding(self, product: str, content: str):
        self.create(f"{PUBLIC_WEBSITES_PATH}/{EMBEDDINGS_PATH}_{product}/embeddings.json", content)
        
    def create(self, file_name: str, content: str):
        new_blob = self.bucket.blob(f"{file_name}")
        new_blob.content_type = "text/plain"
        new_blob.upload_from_string(content)

    def get_embeddings_path(self, product: str):
        return f"gs://{self.bucket_name}/{PUBLIC_WEBSITES_PATH}/{EMBEDDINGS_PATH}_{product}"
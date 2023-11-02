from pydantic import BaseModel

class PublicURL(BaseModel):
    index_name: str
    product_name: str
    url: str
from pydantic import BaseModel

class PublicURL(BaseModel):
    index_name: str
    prefix_name: str
    url: str
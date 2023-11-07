from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from src.model import PublicURL
from src.gcs_service import GCSService
from src.index_service import IndexService
from src.background import index_update
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from os import getenv
disable_warnings(InsecureRequestWarning)

app = FastAPI()
PROJECT_ID = getenv("PROJECT_ID")
REGION = getenv("REGION")

async def get_index_service():
    return IndexService()

# Create a route to handle GET requests on root
@app.get("/")
async def root():
    return 'You are calling Public Websites Index Updation'

@app.post("/api/v1/public_url")
async def add_gcp_product(
        public_website: PublicURL, 
        background_tasks: BackgroundTasks, 
        index_service: IndexService = Depends(get_index_service),
    ):
    if not public_website.url.endswith("sitemap.xml"): 
        raise HTTPException(status_code=400, detail="URL should be a valid sitemap.xml")
    gcs_service = GCSService(public_website.index_name)
    background_tasks.add_task(index_update, public_website, gcs_service, index_service)
    return f"Index update is running, please check for logs/progress https://console.cloud.google.com/run/detail/{REGION}/datapipeline/logs?project={PROJECT_ID}"
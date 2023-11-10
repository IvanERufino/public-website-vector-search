from src.logger import logger
from src.gcp_documents import chunk_documents, create_embeddings, load_urls, parse_generic_sitemap, filter_sites
from src.gcs_service import GCSService
from src.index_service import IndexService
from src.model import PublicURL

def index_update(genericUrl: PublicURL, gcs_service: GCSService, index_service: IndexService):
        index_name = genericUrl.index_name
        name = genericUrl.prefix_name
        url = genericUrl.url
        
        logger.log_text(f"[{name}] Public URL index updation has started for: {url}")

        logger.log_text(f"[{name}] Getting sitemap and filtering...")
        sites = parse_generic_sitemap(url)
        sites_filtered = filter_sites(sites)

        logger.log_text(f"[{name}] Loading URLs...")
        documents = load_urls(sites_filtered)

        logger.log_text(f"[{name}] Generating chunks...")
        chunks = chunk_documents(documents)

        logger.log_text(f"[{name}] Creating embeddings...")
        create_embeddings(name, chunks, gcs_service)

        logger.log_text(f"[{name}] Updating GCP documents index")
        storage_path = gcs_service.get_embeddings_path(name)
        if gcs_service.new_bucket:
            logger.log_text(f"[{name}] Creating new index")
            index = index_service.create_index(index_name, storage_path)
            logger.log_text(f"[{name}] Creating new index endpoint")
            endpoint = index_service.create_index_endpoint(index_name)
            logger.log_text(f"[{name}] Deploying new index")
            index_service.deploy_index(index, endpoint)
        else:
            logger.log_text(f"[{name}] Updating index")
            index_service.update_index(storage_path, index_name)
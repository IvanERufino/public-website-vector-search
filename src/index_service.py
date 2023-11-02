from google.cloud import aiplatform
from google.cloud.aiplatform import MatchingEngineIndex, MatchingEngineIndexEndpoint
from os import getenv

REGION = getenv("REGION")
DIMENSIONS=768
DISTANCE_MEASURE='DOT_PRODUCT_DISTANCE'
NEIGHBORS_COUNT=150

class IndexService:
    def create_index(self, display_name: str, storage_path: str):
        return aiplatform.MatchingEngineIndex.create_tree_ah_index(
            display_name=display_name,
            contents_delta_uri=storage_path,
            dimensions=DIMENSIONS,
            approximate_neighbors_count=NEIGHBORS_COUNT,
            distance_measure_type=DISTANCE_MEASURE)
    
    def update_index(self, storage_path: str, index_name: str):
        index = ""
        for mei in MatchingEngineIndex.list(location=REGION):
            if mei.displayName == index_name:
                index = mei.name
        index = aiplatform.MatchingEngineIndex(index_name=index)
        index.update_embeddings(
            contents_delta_uri=storage_path,
        )
    
    def create_index_endpoint(self, display_name: str):
        return aiplatform.MatchingEngineIndexEndpoint.create(
            display_name=display_name,
            description=display_name,
        )

    def deploy_index(self, index: MatchingEngineIndex, endpoint: MatchingEngineIndexEndpoint):
        endpoint.deploy_index(
            index=index, deployed_index_id=index.display_name)
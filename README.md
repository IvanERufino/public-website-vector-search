# Public Website Vector Search

## Architecture

![](/images/Public-website-vector-search.png)

## Endpoints

### Public URL load

* Path: /api/v1/public_url
* Verb: POST
* Body: 
```
{
    index_name: str = This parameter will match your index and indexEndpoint DisplayName and your GCS Bucket. In case a GCS Bucket with that name doesn't exist a new one will be created, as well as a new index
    url: str = The URL which content is going to be embedded
    product: str = Its a standard name you'll give your URL. It will be used as a tag on Cloud log, to track the progress of your job, as well as to create a folder inside your GCS Bucket, which will later on store the embeddings
}
```
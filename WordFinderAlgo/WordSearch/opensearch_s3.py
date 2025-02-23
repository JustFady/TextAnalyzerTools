import sys
import json
import boto3 
from elasticsearch import Elasticsearch # type: ignore

# Elasticsearch connection details
ES_HOST = 'endpoint' # can't access this from aws troubles
ES_PORT = 443  # Default port 9920
INDEX_NAME = 'test-opensearch'

# AWS S3 configuration
S3_BUCKET = 's3test4589'  
S3_PREFIX = 'https://s3test4589.s3.amazonaws.com/'

def get_es_client():
    return Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}]) # can't connect due to endpoint issues

def index_s3_data(es_client):
    s3_client = boto3.client('s3', 'opensearch') # s3 client using opensearch from boto3 library 

 #https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=S3_PREFIX)

    for obj in response.get('Contents', []):
        file_key = obj['Key']
        
        s3_object = s3_client.get_object(Bucket=S3_BUCKET, Key=file_key)
        body = s3_object['Body'].read()
        data = body.decode('utf-8')
        
        json_data = json.loads(data) # from s3 bucket, also can be used to read from local machine

        for index, item in enumerate(json_data):
            es_client.index(index=INDEX_NAME, id=index, body=item)
        print(f"Indexed data from {file_key}")

def search_es(es_client, query):
    # from aws documentation
    search_query = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["*"] # search all fields
            }
        }
    }

    #https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-access-permissions.html
    #search for term and put it in results
    result = es_client.search(index=INDEX_NAME, body=search_query)

    # Check if any results were found
    if not result['hits']['hits']:
        print(f"No results found for '{query}'.")
    else:
        # Print result
        print(f"Search results for '{query}':")
        for hit in result['hits']['hits']:
            print(json.dumps(hit['_source'], indent=2))

if __name__ == "__main__":
    search_term = sys.argv[1]
    es_client = get_es_client()
    search_es(es_client, search_term)

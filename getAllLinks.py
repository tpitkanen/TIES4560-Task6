import json
import boto3

from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
table_collections = dynamodb.Table('collections')
table_links = dynamodb.Table('links')

def lambda_handler(event, context):
    # Check path parameters
    path_collection_id = None
    try:
        path_params = event.get('pathParameters')
        path_collection_id = path_params.get('collectionId')
    except AttributeError:
        pass
    if path_collection_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing path parameter: path_collection_id')
        }
    
    # Check if collection exists
    response_collection = table_collections.get_item(
        Key={
            'collection_id': path_collection_id
        }
    )
    collection = response_collection.get('Item')
    if collection is None:
        return {
            'statusCode': 404,
            'body': json.dumps('Collection found')
        }
    
    # Get all links for collection
    collection_links = []
    scan = table_links.scan(
        FilterExpression=Attr('collection_id').eq(path_collection_id)
    )
    for link in scan.get('Items'):
        collection_links.append(link)
    collection['collection_links'] = collection_links
    
    return {
        'statusCode': 200,
        'body': json.dumps(collection)
    }

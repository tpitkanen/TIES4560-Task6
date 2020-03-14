import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('collections')

def lambda_handler(event, context):
    # Check path parameters
    collection_id = None
    try:
        path_params = event.get('pathParameters')
        collection_id = path_params.get('collectionId')
    except AttributeError:
        pass
    if collection_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing path parameter: collection_id')
        }
    
    # Get collection
    response = table.get_item(
        Key={
            'collection_id': collection_id
        }
    )
    item = response.get('Item')
    if item is None:
        return {
            'statusCode': 404,
            'body': json.dumps('Not found')
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }

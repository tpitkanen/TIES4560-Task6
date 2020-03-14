import json
import boto3

from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
table_collections = dynamodb.Table('collections')
table_links = dynamodb.Table('links')

def lambda_handler(event, context):
    # Get path parameters
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

    # Delete collection
    response = table_collections.delete_item(
        Key={
            'collection_id': collection_id
        }
    )
    
    # Delete links in collection
    scan = table_links.scan(
        FilterExpression=Attr('collection_id').eq(collection_id)
    )
    with table_links.batch_writer() as batch:
        for each in scan.get('Items'):
            batch.delete_item(
                Key={
                    'link_id': each.get('link_id')
                }
            )

    return {
        'statusCode': 204
    }

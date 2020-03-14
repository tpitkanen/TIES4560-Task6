import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_links = dynamodb.Table('links')

def lambda_handler(event, context):
    # Check path parameters
    collection_id = None
    link_id = None
    try:
        path_params = event.get('pathParameters')
        collection_id = path_params.get('collectionId')
        link_id = path_params.get('linkId')
    except AttributeError:
        pass
    if collection_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing path parameter: collection_id')
        }
    if link_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing path parameter: link_id')
        }
    
    # Get link
    response = table_links.get_item(
        Key={
            'link_id': link_id
        }
    )
    link = response.get('Item')
    if link is not None and link.get('collection_id') == collection_id:
        return {
            'statusCode': 200,
            'body': json.dumps(link)
        }

    return {
        'statusCode': 404,
        'body': json.dumps('Not found')
    }

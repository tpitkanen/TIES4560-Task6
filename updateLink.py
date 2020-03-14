import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_collections = dynamodb.Table('collections')
table_links = dynamodb.Table('links')

def lambda_handler(event, context):
    # Check path parameters
    path_collection_id = None
    path_link_id = None
    try:
        path_params = event.get('pathParameters')
        path_collection_id = path_params.get('collectionId')
        path_link_id = path_params.get('linkId')
    except AttributeError:
        pass
    if path_collection_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing path parameter: path_collection_id')
        }
    if path_link_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing path parameter: path_link_id')
        }

    # Check that link exists
    response = table_links.get_item(
        Key={
            'link_id': path_link_id
        }
    )
    item = response.get('Item')
    if item is None:
        return {
            'statusCode': 404,
            'body': json.dumps('Link not found')
        }
    
    # Check that path collection_id and body collection_id match
    body = json.loads(event.get('body'))
    body_collection_id = body.get('collection_id')
    if path_collection_id != body_collection_id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Path collection_id did not match body collection_id',
                'path_collection_id': path_collection_id,
                'body_collection_id': body_collection_id
            })
        }

    # Check that path link_id and body link_id match
    body_link_id = body.get('link_id')
    if path_link_id != body_link_id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Path link_id did not match body link_id',
                'path_link_id': path_link_id,
                'body_link_id': body_link_id
            })
        }
    
    # Check for required attributes
    required_attributes = ['link_id', 'collection_id', 'description', 'url']
    missing_attributes = []
    for attrib in required_attributes:
        if body.get(attrib) is None:
            missing_attributes.append(attrib)
    if len(missing_attributes) > 0:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Missing required attributes',
                'missingAttributes': missing_attributes
            })
        }
    
    # Update item
    table_links.put_item(Item=body)
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }

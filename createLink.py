import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_collections = dynamodb.Table('collections')
table_links = dynamodb.Table('links')

def lambda_handler(event, context):
    # Check for required attributes
    required_attributes = ['link_id', 'collection_id', 'description', 'url']
    missing_attributes = []
    body = json.loads(event.get('body'))
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
        
    # Check that path collection_id and body collection_id match
    link_id = body.get('link_id')
    collection_id = body.get('collection_id')
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
    if path_collection_id != collection_id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Path id did not match collection_id in body',
                'path_collection_id': path_collection_id,
                'collection_id': collection_id
            })
        }
    
    # Check that link_id is not already in use
    response_link = table_links.get_item(
        Key={
            'link_id': link_id
        }
    )
    item = response_link.get('Item')
    if item is not None:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Link with link_id already exists',
                'link_id': link_id
            })
        }
    
    # Check that collection_id refers to an existing collection
    response_collection = table_collections.get_item(
        Key={
            'collection_id': collection_id
        }
    )
    collection = response_collection.get('Item')
    if collection is None:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'collection_id refers to a non-existent collection',
                'collection_id': collection_id
            })
        }
    
    # Create link
    table_links.put_item(Item=body)
    return {
        'statusCode': 201,
        'body': json.dumps(body)
    }

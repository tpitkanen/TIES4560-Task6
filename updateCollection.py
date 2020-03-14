import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('collections')

def lambda_handler(event, context):
    # Check path parameters
    path_id = None
    try:
        path_params = event.get('pathParameters')
        path_id = path_params.get('collectionId')
    except AttributeError:
        pass
    if path_id is None:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing path parameter: path_id')
        }
    
    # Check that collection exists before updating
    response = table.get_item(
        Key={
            'collection_id': path_id
        }
    )
    item = response.get('Item')
    if item is None:
        return {
            'statusCode': 404,
            'body': json.dumps('Not found')
        }
        
    # Check that path id and request body id match
    body = json.loads(event.get('body'))
    body_id = body.get('collection_id')
    if path_id != body_id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Path id did not match collection_id in body',
                'path_id': path_id,
                'collection_id': body_id
            })
        }
    
    # Check for required attributes
    required_attributes = ['collection_id', 'collection_name']
    missing_attributes = []
    for attrib in attributes:
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
    table.put_item(Item=body)
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }

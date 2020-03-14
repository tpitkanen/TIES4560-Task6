import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('collections')

def lambda_handler(event, context):
    # Check for required attributes
    required_attributes = ['collection_id', 'collection_name']
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
    
    # Check that collection_id is not already in use
    collection_id = body.get('collection_id')
    response = table.get_item(
        Key={
        'collection_id': collection_id
        }
    )
    item = response.get('Item')
    if item is not None:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Collection with collection_id already exists',
                'collection_id': collection_id
            })
        }

    # Create collection
    table.put_item(Item=body)
    return {
        'statusCode': 201,
        'body': json.dumps(body)
    }

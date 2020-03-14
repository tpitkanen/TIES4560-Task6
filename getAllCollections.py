import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_collections = dynamodb.Table('collections')

def lambda_handler(event, context):
    # Get all collections
    collections = []
    scan = table_collections.scan()
    for collection in scan.get('Items'):
        collections.append(collection)
    
    return {
        'statusCode': 200,
        'body': json.dumps(collections)
    }

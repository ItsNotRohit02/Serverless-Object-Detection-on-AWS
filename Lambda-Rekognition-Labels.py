import json
import boto3

s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = 'DynamoDBTableName'

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    response = rekognition_client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': object_key
            }
        },
        MaxLabels=10,
        MinConfidence=75
    )

    labels = [label['Name'] for label in response['Labels']]
    
    labels += [None] * (10 - len(labels))

    dynamodb_item = {
        'PartitionKeyName': object_key,
        'Label1': labels[0],
        'Label2': labels[1],
        'Label3': labels[2],
        'Label4': labels[3],
        'Label5': labels[4],
        'Label6': labels[5],
        'Label7': labels[6],
        'Label8': labels[7],
        'Label9': labels[8]
    }

    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=dynamodb_item)

    return {
        'statusCode': 200,
        'body': json.dumps(f"Labels for {object_key} inserted into DynamoDB.")
    }
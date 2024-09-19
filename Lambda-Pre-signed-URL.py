import json
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = "S3-Bucket-Name"
    key = event['queryStringParameters']['file_name']

    presigned_url = s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': bucket_name,
            'Key': key,
            'ContentType': 'image/jpeg'
        },
        ExpiresIn=600
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps({"presigned_url": presigned_url}),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*", 
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
    }
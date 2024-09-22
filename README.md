# Object Detection WebApp on AWS

## Project Overview

This project involves building a cloud-based object detection system using AWS services. The system will allow users to upload images, process them using Amazon Rekognition, and store the detected labels in a DynamoDB table. The architecture leverages AWS Lambda, API Gateway, S3, EC2, and Auto Scaling to create a scalable and efficient solution.

## Architecture Diagram
[Architecture Diagram](Architecture-Diagram.jpg)

### Project Flow

1. **User Interface**:
    
    Users access a web interface hosted on an EC2 instance. This interface provides a form to upload images.
    
2. **Image Upload**:
    
    When a user selects an image and submits the form, the web interface sends a request to an API Gateway endpoint to get a pre-signed URL for uploading the image to an S3 bucket.
    
3. **Generate Pre-Signed URL**:
    
    An AWS Lambda function (`LambdaPreSignedURL`) is invoked by the API Gateway to generate a pre-signed URL for the S3 bucket. The pre-signed URL is returned to the web interface.
    
4. **Upload Image to S3**:
    
    The web interface uses the pre-signed URL to upload the image directly to the S3 bucket (`ImageS3Bucket`).
    
5. **S3 Event Notification**:
    
    Once the image is uploaded to the S3 bucket, an S3 event is triggered (configured manually to avoid circular dependencies). This event invokes another Lambda function (`LambdaRekognitionLabels`).
    
6. **Image Processing with Rekognition**:
    
    The `LambdaRekognitionLabels` function processes the image using Amazon Rekognition to detect labels. The detected labels are then formatted and stored in a DynamoDB table (`LabelsDynamoDBTable`).
    
7. **Store Labels in DynamoDB**:
    
    The labels detected by Rekognition are stored in the DynamoDB table along with the image name as the primary key.
    
8. **Auto Scaling and EC2 Hosting**:
    
    The web interface is hosted on an EC2 instance, which is part of an Auto Scaling Group (`MyAutoScalingGroup`) to ensure high availability and scalability. The EC2 instances are launched using a predefined launch template (`MyLaunchTemplate`).
    
9. **Security and Permissions**:
    
    The project uses various IAM roles and policies to ensure that AWS services interact securely. This includes permissions for Lambda functions to access S3, Rekognition, DynamoDB, and CloudWatch Logs.
    

### AWS CloudFormation Template Components

- **Parameters**:
    - `VPCID`: VPC where resources will be launched.
    - `SubnetIds`: List of subnet IDs for the Auto Scaling Group.
- **Resources**:
    - `ImageS3Bucket`: S3 bucket to store uploaded images with CORS configuration.
    - `LabelsDynamoDBTable`: DynamoDB table to store image labels.
    - `LambdaPreSignedURL`: Lambda function to generate pre-signed URLs for S3 uploads.
    - `LambdaRekognitionLabels`: Lambda function to process images using Rekognition and store labels in DynamoDB.
    - `MyApiGatewayRestApi`: API Gateway to handle requests.
    - `ApiGatewayResourceUpload`: API Gateway resource for upload.
    - `ApiGatewayMethodUploadGet`: Method for API Gateway to get pre-signed URL.
    - `ApiGatewayCORS`: CORS configuration for API Gateway.
    - `ApiGatewayDeploymentProd`: Deployment configuration for API Gateway.
    - `LambdaInvokePermission`: Permission for API Gateway to invoke Lambda.
    - `EC2SecurityGroup`: Security group for EC2 instances.
    - `ALBSecurityGroup`: Security group for Application Load Balancer.
    - `MyLaunchTemplate`: Launch template for EC2 instances.
    - `MyAutoScalingGroup`: Auto Scaling group configuration.
    - `ScalingPolicy`: Scaling policy for Auto Scaling group.
    - `LambdaPermissionForS3`: Permission for S3 to invoke Lambda.
    - `LambdaPreSignedIAMRole`: IAM role for `LambdaPreSignedURL`.
    - `LambdaRekognitionIAMRole`: IAM role for `LambdaRekognitionLabels`.
- **Outputs**:
    - `ApiUrl`: URL of the API Gateway.

### Deployment and Manual Configuration Steps

1. **Deploy CloudFormation Stack**:
    
    Deploy the CloudFormation stack using the provided template to create all necessary resources.
    
2. **Configure S3 Event Notification**:
    
    Manually configure the S3 bucket to trigger the `LambdaRekognitionLabels` function on object creation events to avoid circular dependencies.
    
3. **Update Web Interface**:
    
    Ensure the web interface is correctly pointing to the deployed API Gateway URL for requesting pre-signed URLs.
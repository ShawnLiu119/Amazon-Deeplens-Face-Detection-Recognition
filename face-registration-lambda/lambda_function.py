import json
from decimal import Decimal
import boto3

dynamodb = boto3.client('dynamodb', region_name='us-east-1')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition', region_name='us-east-1')

face_collection = "Face"

#helper function
def index_faces(bucket, key):
    response = rekognition.index_faces(
        Image={"S3Object":
            {"Bucket": bucket,
            "Name": key}},
            CollectionId='Face')
    print ('Results for ' + key) 	
    print('Faces indexed:')
    for faceRecord in response['FaceRecords']:
        print('  Face ID: ' + faceRecord['Face']['FaceId'])
        print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))
    return response
    
def update_index(tableName,faceId, fullName):
    response = dynamodb.put_item(
        TableName=tableName,
        Item={
            'faceID': {'S': faceId},
            'FullName': {'S': fullName}
            }
        ) 
        
def lambda_handler(event, context):
    # TODO implement
    bucket = event['Records'][0]['s3']['bucket']['name']
    key =event['Records'][0]['s3']['object']['key']
    
    try:
        response = index_faces(bucket, key)
        #commut faceId and full name object metadat to DynamoDB
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']
            
            ret = s3.head_object(Bucket=bucket,Key=key)
            personFullName = ret['Metadata']['fullname']
            
            update_index('Face',faceId,personFullName)
        
        #print response to console
        print(response)
        
        return(response)
        
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket))
        raise e

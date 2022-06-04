'''
        Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
        SPDX-License-Identifier: MIT-0
'''
import json
import boto3
import time
import os
import re
from boto3 import resource
from boto3.dynamodb.conditions import Key
import subprocess
from tempfile import gettempdir
from contextlib import closing
from botocore.exceptions import BotoCoreError, ClientError
import sys


s3 = boto3.client('s3')
rekognition = boto3.client('rekognition', region_name='us-east-1')
iotClient = boto3.client('iot-data')
polly= boto3.client('polly')

dynamodb =boto3.client('dynamodb', region_name='us-east-1')


face_collection = "Face" # Name of the face collection that the AWS Rekognition uses
face_match_threshold = 70 # Match Threshold for the faces to be concidered the same person
logging_table = 'logs' # DynamoDB table name for the log files



def lambda_handler(event, context):

    utime = str(int(time.time())) #Current Unix Time   
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']  
    print(event)
    image = {
        'S3Object': {
            'Bucket': bucket,
            'Name': key,
            }
        }

    message = detect_faces(image, bucket, key)
    
    play_msg(message)
    
    return message

def detect_faces(image, bucket, key):

    # Checks if user face is already registered in rekongtion collection
    response = rekognition.search_faces_by_image(CollectionId=face_collection, Image=image,
                                              FaceMatchThreshold=face_match_threshold, MaxFaces=1)
                                              
    if len(response['FaceMatches']) >0:
        for match in response['FaceMatches']:
            face =dynamodb.get_item(
                TableName = 'Face',
                Key = {'faceID': {'S': match['Face']['FaceId']}})
            
            if 'Item' in face:
                person = face['Item']['FullName']['S']
            else:
                person ='no match found'
        
            print(match['Face']['FaceId'], match['Face']['Confidence'], person)
            
            return person
    

def play_msg(person):
    msg_dic ={
        'Enya': 'Hello, Enya, let us dance',
        'weina': 'Hello, weina, do you love Enya?',
        'shawn': 'shawn, time to play with Enya',
        'papa': 'papa, who is your grandaughter?',
        'laolao': 'law law, Enya wants cheese'
    }
    
    if person == 'Enya':
        play(msg_dic['Enya'])
    elif person == 'weina':
        play(msg_dic['weina'])
    elif person == 'papa':
        play(msg_dic['papa'])
    elif person == 'laolao':
        play(msg_dic['laolao'])
    else:
        play(msg_dic['shawn'])
    
    
        
def play(msg):
    try:
    # Request speech synthesis
        response = polly.synthesize_speech(Text=msg, SampleRate = "16000", OutputFormat="mp3", VoiceId="Joanna")
        print(response)
        
        mp3Key = msg + '.mp3'
        s3Response = s3.put_object(
            Bucket = 'deeplens-facerecognition-t1',
            Key=mp3Key,
            Body = response['AudioStream'].read(),
            ContentType = 'audio/mpeg'
            )
        print('output polly')
            
    except (BotoCoreError, ClientError) as error:
    # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)
        
        
        
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(gettempdir(), "speech.mp3")
            
            try:
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(-1)
                
    else:
        print("Could not stream audio")
        sys.exit(-1)
        
  
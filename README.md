# AWS_Deeplens_Face_Recognition_Project

##Introduction & Problem Definition
This project aims at developing a computer vision application with capability of detecting and recognizing faces based on ML algorithms and AWS cloud services and deployed the application on Amazon DeepLens as edge device.

##Architecture & Environment Overview
The programmatic components including primarily ML models and Lambda functions are developed with Python 3.7 runtime under AWS Linux ecosystem. The application workflow runs dependent on the collaboration between edge and cloud section. The graph below demonstrates the workflow diagram.

![image](https://user-images.githubusercontent.com/43327902/185544267-94f5ec5c-7f2b-4c58-ac69-65b159d5f573.png)

The edge, DeepLens camera, takes care of face detection duty with a computer vision model and Lambda function deployed. The model is tasked to conduct image analysis job in consecutive basis and the Lambda function uploads the image if any face is detected. Once the image is uploaded to the assigned S3 bucket on the cloud. another Lambda function is triggered to call for Amazon Rekognition service to conduct image analysis and match the faced detected from the uploaded image with ones registered in DynamoDB collection, The DynamoDB keeps the record of index faces with FaceID, pattern and label for each. If a match is returned, the Lambda function will call for Polly’s text-to-speech service to generate welcome message as mp3 file and upload it to S3 bucket.

## Experimental Evaluation
Multiple tests have been conducted. Since 16 images of 5 faces have been indexed and registered with DynamoDB to make sure the pattern of each face is fully learned by Rekognition, all tests work out (5/5 rate) given the small sample of indexed faces. Below are the logs documented by AWS CloudWatch service regarding the label identification and Polly output process.

![image](https://user-images.githubusercontent.com/43327902/185544335-86c35005-e58a-498c-97b6-1d3fad41fe8f.png)

## Related Work
There are several trials which perform similar features but were built upon Python 2.7 runtime back in 2018 Amazon re:Invent. OneEye, developed by Dr. Yazdan Shivany’s team, is capable of detecting customer face and pulling out the matched customer profile from backend database based on AWS ecosystem (link to more details). DeepLens Family Assistant is another similar face recognition application designed based on AWS computer vision algorithm but extend with additional front-end user interface using Amazon Elastic Beanstalk.

## **Development Environment**
python 3.7, AWS Linux

## **Face Detection Model Overview**

![This is an image](model.PNG)

import json
import boto3

# adding the s3 client
s3 = boto3.client('s3',region_name='us-east-1')
bucket_name = 'PASTE YOUR BUCKET NAME HERE'

#adding the SNS client
sns = boto3.client('sns')
sns_topic_arn = "PASTE TOPIC ARN HERE"

#adding the SQS client
sqs = boto3.client('sqs')
queque_url = "PASTE SQS URL HERE"

def lambda_handler(event, context):
    print("Loading Lambda function ......\n")
    body = event["Records"][0]["body"]
    messageId = event["Records"][0]["messageId"]
    # records variable is a list
    # this array only contains one value (0) ... currently looks like this [0]
    
    print(body)
    print(type(body))
    
    new_body = str(body)
    s3key = str(messageId) + ".json"
    uploadByteStream = bytes(json.dumps(event).encode('UTF-8'))
    s3.put_object(Body=uploadByteStream,Bucket=bucket_name,Key=s3key)
    print("....SNS TIME.....")
    sns_response = sns.publish(TopicArn=sns_topic_arn,Message=new_body,Subject="New message in SQS")

    return "SUCCESS!!!!"
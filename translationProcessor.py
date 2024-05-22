import json
import boto3
import googletrans
from googletrans import Translator
import datetime
from botocore.exceptions import ClientError

#add in the curret date and time
current_time = datetime.datetime.now()

# adding the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PASTE YOUR TABLE HERE')

# adding the s3 client
s3 = boto3.client('s3',region_name='us-east-1')
bucket_name = 'PASTE YOUR BUCKET HERE'

#adding the SQS client
sqs = boto3.client('sqs')
queque_url = "PASTE YOUR SQS QUEUE HERE"

def lambda_handler(event, context):
    print('LOADING LAMBDA FUNCTION......', current_time)
    #determine the HTTP method
    http_method = event.get('httpMethod')

    all_lang=googletrans.LANGUAGES
    translator = Translator()
    
    if http_method == "POST":
        # define the item to be inserted
        body = json.loads(event.get("body"))
        
        #the http body now becomes a dictionary and looks like the following:
        """
        {
            "translationId":10,
            "src":"en",
            "dest":"es",
            "text":"Hello world!"
        }
        """
        finalTranslation = translator.translate(body["text"],src=body["src"],dest=body["dest"])
        
        finalText = finalTranslation.text
        
        item = {'requestNumber': body["translationId"],'original_text':body["text"],'translated_text':finalText}

        try:
            response = table.put_item(Item=item)
            print('PutItem succeeded: ', response)
        except Exception as e:
            print ("Error inserting item: ", e)
        
        # put the original text and translated text into a .json and upload it into an S3 bucket
        # name the .json file a unique-name by date or time-stamp for example 04132024.txt???
        s3key = body["translationId"]
        fileName = str(s3key) + '.json'
        uploadByteStream = bytes(json.dumps(body).encode('UTF-8'))    
        s3.put_object(Body=uploadByteStream, Bucket=bucket_name, Key=fileName)

        message = {"translationId":body["translationId"],"originalTranslation":body["text"]}
        
        sqs_reponse = sqs.send_message(QueueUrl=queque_url,MessageBody=json.dumps(message))

        # return the HTTP response object
        return {
            "statusCode": 200,
            "body":finalText
        }
    
    #start of another GET method 
    elif http_method == "GET":
        new_response = table.scan()
        items=new_response['Items']
        return {
            "statusCode":200,
            "body":str(items)
        }
    else:
        fail = 'The CRUD operation you requested is not set up'
        return fail

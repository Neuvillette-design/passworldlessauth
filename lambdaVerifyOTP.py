import boto3
import time
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserOTPs')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    email = body['email']
    user_otp = body['otp']
    response = table.get_item(Key={'email': email})
    
    if 'Item' not in response:
        return {'statusCode': 400, 'body': json.dumps('No OTP found')}
    
    db_otp = response['Item']['otp']
    expiry = response['Item']['expires_at']
    
    if time.time() > expiry:
        return {'statusCode': 400, 'body': json.dumps('OTP Expired')}
    
    if user_otp == db_otp:
        return {'statusCode': 200, 'body': json.dumps('Access Granted!')}
    else:
        return {'statusCode': 400, 'body': json.dumps('Invalid OTP')}
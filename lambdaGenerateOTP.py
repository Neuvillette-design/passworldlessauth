import boto3
import random
import time
import json

cognito = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')
table = dynamodb.Table('UserOTPs')

USER_POOL_ID = 'ap-south-1_uO6hdaW7v'
def lambda_handler(event, context):
    body = json.loads(event['body'])
    email = body['email']
    try:
        cognito.admin_get_user(
            UserPoolId=USER_POOL_ID,
            Username=email
        )
        otp = str(random.randint(100000, 999999))
    
        expiry = int(time.time()) + 300
    
        table.put_item(Item={
            'email': email,
            'otp': otp,
            'expires_at': expiry
    })
    
        ses.send_email(
            Source='YOUR_EMAIL_ADDRESS',
            Destination={'ToAddresses': [email]},
            Message={
                'Subject': {'Data': 'Your Login Code'},
                'Body': {'Text': {'Data': f'Your code is {otp}. It expires in 5 minutes.'}}
            }
    )
    
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User verified in Cognito, OTP sent!'})
                }
    except cognito.exceptions.UserNotFoundException:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'You are not on the guest list! Please sign up.'})
        }
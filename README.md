Serverless Passwordless Authenticator (AWS + Streamlit)

A secure, fully serverless authentication system built on AWS. This project replaces traditional passwords with email-delivered One-Time Passwords (OTP), using Amazon Cognito for identity management and Streamlit for a modern user-interface.

Overview

Traditional passwords are often the weakest link in security. This solution allows users to authenticate using a secure 6-digit code sent to their verified email address.

Key Features

Passwordless Flow: No passwords stored, managed, or leaked.

Zero Infrastructure: Built entirely on AWS Serverless (Lambda, API Gateway, DynamoDB).

Identity Guard: Integration with AWS Cognito ensures only authorized users can request OTPs.

Auto-Expiry: OTPs automatically self-destruct after 5 minutes using DynamoDB TTL.

Modern UI: A clean, responsive dashboard built with Streamlit.

Architecture

Streamlit UI: The front-end where users register or request login.

Amazon API Gateway: Exposes RESTful endpoints (/signup, /request, /verify).

AWS Lambda:

SignUpUser: Registers users in Cognito with a secure dummy password.

GenerateOTP: Validates the user in Cognito, generates a 6-digit code, and triggers SES.

VerifyOTP: Matches the user-provided code against the DynamoDB record.

Amazon Cognito: Acts as the master directory of registered users.

Amazon DynamoDB: Stores temporary OTPs with a Time-To-Live (TTL) for security.

Amazon SES: Delivers the OTP directly to the user's inbox.

Tech Stack

Frontend: Streamlit

Compute: AWS Lambda (Python 3.12)

API Management: Amazon API Gateway

Identity: Amazon Cognito

Database: Amazon DynamoDB

Email: Amazon SES

Logging: Amazon CloudWatch

Setup & Installation

1. Database Setup

Create a DynamoDB table named UserOTPs:

Partition Key: email (String)

TTL Attribute: expires_at

2. Identity Pool

Create a Cognito User Pool:

Enable Email as a sign-in attribute.

Create an App Client and note the AppClientID.

Backend Logic (AWS Lambda)

To minimize complexity and operational overhead, the system's logic is consolidated into two high-performance Python Lambda functions.

1. GenerateOTP

The Workflow:

Cognito Check: It first attempts to locate the user in the Cognito User Pool.

Auto-Registration: If the user doesn't exist, it utilizes AdminCreateUser to register them instantly.

Security: Generates a 6-digit OTP and an expiry timestamp ($CurrentTime + 300s$).

Storage & Dispatch: Simultaneously writes the OTP to DynamoDB and dispatches a secure email via Amazon SES.

Permissions: cognito-idp:AdminCreateUser, dynamodb:PutItem, ses:SendEmail.

2. VerifyOTP

The Workflow:

Fetch: Pulls the record from DynamoDB using the email as the Partition Key.

Validate: Compares the user's input with the stored OTP.

Expiry Check: Compares the current epoch time against the expires_at attribute to prevent "replay attacks" or stale logins.

Authorize: Returns a success signal to Streamlit to trigger the video redirect.

Permissions: dynamodb:GetItem, dynamodb:DeleteItem (to clean up the OTP after use).

API Gateway ConfigurationAmazon 

API Gateway serves as the secure "Front Door" for the Streamlit application. 

We followed these specific steps to expose the Lambda logic to the web:

REST API Creation: Built a standard REST API named PasswordlessAuthAPI.

Resource Mapping: Created a /request resource for the GenerateOTP Lambda and created a /verify resource for the VerifyOTP Lambda.

Method Configuration: Both resources were set to the POST method to ensure user emails and OTPs are sent securely in the request body rather than the URL.

CORS (Cross-Origin Resource Sharing): 

Crucial Step: Enabled CORS on both resources to allow the Streamlit frontend (running on a different domain/local port) to communicate with the AWS backend. Configured allowed headers (Content-Type, X-Amz-Date, Authorization).

Deployment: Created a Deployment Stage named prod to generate the Invoke URL used in the Streamlit first1.py.

Run Frontend

Bash
# Install dependencies
pip install streamlit requests boto3

# Run the app
streamlit run first1.py

Security Considerations

Least Privilege: All Lambda functions operate under IAM roles with minimal permissions.

Sandbox Safety: SES is configured in Sandbox mode for testing; recipient emails must be verified.

Data Integrity: OTPs are never logged in CloudWatch, only process success/failure metrics are recorded.

Success State
Upon successful verification, the user is automatically redirected to the protected content (e.g., an embedded YouTube video).

https://passworldlessapp-samael.streamlit.app/

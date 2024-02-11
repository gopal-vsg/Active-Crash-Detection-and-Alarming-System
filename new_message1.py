import boto3
import json

# Create a Lambda client
def send_email(image_name):
    client = boto3.client('lambda')

# Define the payload data
    payload_data = {
        "sender_email": "saigopalvallu7@gmail.com",
        "password": "wyedsfshankpetlj",
        "reciever_email": "gopalvalluintern@gmail.com",
        "image_name": image_name,
    # Corrected key name
    }

# Invoke the Lambda function
    response = client.invoke(
        FunctionName='lambda',  # Replace with your Lambda function name
        InvocationType='RequestResponse',
        Payload=json.dumps(payload_data)  # Serialize the payload directly here
    )

# Extract and process the response from the Lambda function
    response_payload = response['Payload'].read()
    print(response_payload.decode('utf-8'))  # Assuming the payload is in UTF-8 encoding

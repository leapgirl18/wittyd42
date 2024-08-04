import os
from flask import Flask, request, jsonify
import requests
import boto3

app = Flask(__name__)

@app.route('/')
def index():
    return 'Service is up and running!'

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Webhook Service!"

@app.route('/generate-url', methods=['POST'])
def generate_url():
    data = request.get_json()
    order_id = data.get('order_id')
    bucket_name = 'dream29'
    object_key = 'Dream-PatywyEbook-Bluept7.15.pdf'

    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

    s3_client = boto3.client('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)

    try:
        # Generate pre-signed URL for S3 object
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_key,
                'ResponseContentDisposition': 'attachment; filename="Dream-PatywyEbook-Bluept7.15.pdf"'
            },
            ExpiresIn=3600
        )
        return jsonify({'url': presigned_url}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/thrivecart-webhook', methods=['POST', 'HEAD'])
def thrivecart_webhook():
    if request.method == 'HEAD':
        return '', 200

    data = request.get_json()
    # Add the Authorization header
    headers = {
        'Authorization': 'your_secret_token',
        'Content-Type': 'application/json'
    }

    # Forward the request to the AWS API Gateway endpoint
    aws_api_gateway_url = 'https://91zswqzovj.execute-api.us-east-1.amazonaws.com/Prod/thrivecart-webhook'
    response = requests.post(aws_api_gateway_url, headers=headers, json=data)
    
    # Return the response from AWS API Gateway
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

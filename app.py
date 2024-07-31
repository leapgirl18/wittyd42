import boto3
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'Service is up and running!'

@app.route('/generate-url', methods=['POST'])
def generate_url():
    data = request.get_json()
    email = data.get('email')
    order_id = data.get('order_id')
    bucket_name = 'dream29'
    object_key = 'Dream-PatywyEbook-Bluept7.15.pdf'

    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

    if not aws_access_key_id or not aws_secret_access_key:
        missing_credentials = {
            'AWS_ACCESS_KEY_ID': 'missing' if not aws_access_key_id else 'present',
            'AWS_SECRET_ACCESS_KEY': 'missing' if not aws_secret_access_key else 'present'
        }
        return jsonify({'error': 'Unable to locate credentials', 'details': missing_credentials}), 500

    s3_client = boto3.client('s3', 
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)

    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_key,
                'ResponseContentDisposition': f'attachment; filename="{order_id}_Dream-PatywyEbook-Bluept7.15.pdf"',
            },
            ExpiresIn=3600
        )
        return jsonify({'url': presigned_url}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/thrivecart-webhook', methods=['POST'])
def thrivecart_webhook():
    data = request.get_json()
    print("Received ThriveCart webhook data:", data)
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True)

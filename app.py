import boto3
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Retrieve AWS credentials from environment variables
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Initialize S3 client with credentials
s3_client = boto3.client('s3', 
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key)

@app.route('/generate-url', methods=['POST'])
def generate_url():
    data = request.get_json()
    email = data.get('email')
    order_id = data.get('order_id')
    bucket_name = 'dream29'
    object_key = 'Dream-PatywyEbook-Bluept7.15.pdf'

    try:
        # Generate pre-signed URL for S3 object
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_key,
                'ResponseContentDisposition': f'attachment; filename="{order_id}_Dream-PatywyEbook-Bluept7.15.pdf"',
            },
            ExpiresIn=3600
        )
        return jsonify({'url': presigned_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == 

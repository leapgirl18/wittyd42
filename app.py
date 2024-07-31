import boto3
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generate-url', methods=['POST'])
def generate_url():
    bucket_name = 'dream29'
    object_key = 'Dream-PatywyEbook-Bluept7.15.pdf'
    expiration = 900  # URL expiration time in seconds (15 minutes)
    
    try:
        # Retrieve AWS credentials from environment variables
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        
        # Initialize the S3 client with the retrieved credentials
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        
        # Generate pre-signed URL
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_key,
                'ResponseContentDisposition': 'attachment',
            },
            ExpiresIn=expiration  # Use ExpiresIn to specify expiration in seconds
        )
        
        # Return the pre-signed URL as part of the response
        return jsonify({'url': presigned_url})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


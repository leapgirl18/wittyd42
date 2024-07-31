# Import necessary libraries
import os
import boto3
from flask import Flask, request, jsonify

# This is a test comment to force a change

app = Flask(__name__)

# Set up S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Endpoint to generate a pre-signed URL
@app.route('/generate-url', methods=['POST'])
def generate_url():
    data = request.get_json()
    email = data['email']
    order_id = data['order_id']

    bucket_name = 'your-bucket-name'
    object_key = 'Dream-PatywyEbook-Bluept7.15.pdf'
    expiration = 3600

    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_key,
                'ResponseContentDisposition': f'attachment; filename="{order_id}_Dream-PatywyEbook-Bluept7.15.pdf"'
            },
            ExpiresIn=expiration
        )
        return jsonify({'url': response})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

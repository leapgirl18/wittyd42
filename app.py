from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

# Load AWS credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')  # Optional, depending on your setup

# Initialize the S3 client
s3_client = boto3.client('s3',
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                         aws_session_token=AWS_SESSION_TOKEN)

@app.route('/generate-url', methods=['POST'])
def generate_url():
    bucket_name = 'your_bucket_name'
    object_key = 'path/to/your/ebook.pdf'
    expiration = 900  # URL expiration time in seconds (15 minutes)

    try:
        # Extract customer information from the request
        data = request.json
        email = data.get('email')
        order_id = data.get('order_id')

        if not email or not order_id:
            return jsonify({'error': "Missing required parameters 'email' or 'order_id'"}), 400

        # Generate unique pre-signed URL
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_key,
                'ResponseContentDisposition': f'attachment; filename="{order_id}_{object_key}"',
            },
            ExpiresIn=expiration
        )

        # Return the pre-signed URL as part of the response
        return jsonify({'url': presigned_url})

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


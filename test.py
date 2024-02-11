import boto3

def upload_file_to_s3(file_path, bucket_name, object_name):
    # Create an S3 client
    s3_client = boto3.client('s3')

    try:
        # Uploads the file to the S3 bucket
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File uploaded successfully to S3 bucket: {bucket_name}")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")

# Example usage
if __name__ == "__main__":
    # Replace these values with your own
    file_path = 'accident_frame.jpg'  # Path to the file you want to upload
    bucket_name = 'cdsgopal'      # Name of your S3 bucket
    object_name = 'accident.jpg'              # Name you want to give to the object in S3

    upload_file_to_s3(file_path, bucket_name, object_name)

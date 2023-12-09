from io import BytesIO

import boto3
from PIL import Image


def list_objects_in_folder(bucket_name, folder_path):
    # Create an S3 client
    s3 = boto3.client("s3")

    # List objects in the specified folder
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)

    # Print the object keys
    print(f"Objects in the folder '{folder_path}':")
    for obj in response.get("Contents", []):
        print(obj["Key"])


def display_s3_image(bucket_name, object_key):
    # Create an S3 client
    s3 = boto3.client("s3")

    # Download the image from S3
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    image_data = response["Body"].read()

    # Open and display the image using Pillow (PIL)
    return Image.open(BytesIO(image_data))

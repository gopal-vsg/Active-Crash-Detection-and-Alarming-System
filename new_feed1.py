from new_message1 import *
import numpy as np
from keras.models import model_from_json
import cv2
import boto3

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# Load weights into the model
loaded_model.load_weights("model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX
count = 1
def running():
    global count
    video = cv2.VideoCapture(0)
    while True:
        ret, frame = video.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        roi = cv2.resize(gray_frame, (250, 250))
        prob = loaded_model.predict(roi[np.newaxis, :, :])
        prob = (round(prob[0][0] * 100, 2))

        if prob > 80:
            print("accident Detected!!")
            cv2.imshow('Frame', frame)
            # Encode the frame as a JPEG image
            success, image_bytes = cv2.imencode('.jpg', frame)
            if success:
                # Convert the encoded image data to bytes
                image_bytes = image_bytes.tobytes()
                # Send email with the image attachment
                file_path = 'accident_frame.jpg'  # Path to the file you want to upload
                bucket_name = 'cdsgopal'  # Name of your S3 bucket
                object_name = f'accident{count}.jpg'  # Name you want to give to the object in S3

                upload_file_to_s3(file_path, bucket_name, object_name)

                cv2.imwrite('accident_frame.jpg', frame)
                send_email(image_name=f"accident{count}.jpg")
                # Pass the file path to the 'send_email_with_photo' function
                count = count + 1

            else:
                print("Failed to encode the image.")

            # Here when the crash is detected that particular frame should be sent to the Azure database

        cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
        cv2.putText(frame, " " + str(prob), (20, 30), font, 1, (255, 255, 0), 2)

        if cv2.waitKey(33) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
def upload_file_to_s3(file_path, bucket_name, object_name):
    # Create an S3 client
    s3_client = boto3.client('s3')

    try:
        # Uploads the file to the S3 bucket
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File uploaded successfully to S3 bucket: {bucket_name}")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
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

if __name__ == '__main__':
    running()

from new_message1 import *
import numpy as np
from keras.models import model_from_json
import cv2

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# Load weights into the model
loaded_model.load_weights("model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

def running():
    video = cv2.VideoCapture('Untitled video - Made with Clipchamp (1).mp4')
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
                sender_email = 'saigopalvallu7@gmail.com'
                sender_password = 'wyedsfshankpetlj'
                receiver_email = 'gopalvalluintern@gmail.com'
                subject = 'Accident Alert!!'
                message = 'Accident Happened, please be at the scene!!'
                cv2.imwrite('accident_frame.jpg', frame)

                # Pass the file path to the 'send_email_with_photo' function
                send_email_with_photo(sender_email, sender_password, receiver_email, subject, message,
                                      'accident_frame.jpg')

            else:
                print("Failed to encode the image.")

            # Here when the crash is detected that particular frame should be sent to the Azure database

        cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
        cv2.putText(frame, " " + str(prob), (20, 30), font, 1, (255, 255, 0), 2)

        if cv2.waitKey(33) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    running()

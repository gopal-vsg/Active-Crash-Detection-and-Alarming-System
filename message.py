import requests

def send_email_with_attachment(img):
    # Base API URL
    base_url = "https://api.mailgun.net/v3/sandbox9914a2aa681f4c53bd52432702b273c7.mailgun.org/messages"

    # Authentication
    auth = ("api", "855466a26286a2e42c540911dce5823f-8c90f339-15a0cf67")

    # Mail data
    data = {
        "from": "Your Name <you@yourdomain.com>",
        "to": ["saigopalvallu7@gmail.com"],  # You can pass a list or a single email address with string data type.
        "subject": "Testing some awesomeness of Mailgun",
        "text": "Mailgun test on the first day of 2019."
    }

    # Attachments
    files = {
        "attachment": ("image.jpg", img, "image/jpeg")  # Specify the correct MIME type if necessary
    }

    # Send email request
    response = requests.post(base_url, auth=auth, data=data, files=files)

    # Check response status
    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print("Failed to send email. Status code:", response.status_code)
        print("Response:", response.text)

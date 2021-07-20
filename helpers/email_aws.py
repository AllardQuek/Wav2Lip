"""
Automate the sending of email with result from AnyTutor video generation. 
If the video generation is successful, an email will be sent with the video as an attachment.
If unsuccessful, an email will be sent with an error message.

"""


import json
import smtplib
import ssl
import os
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def craft_email(sender_email, receiver_email, name, filename):
    subject = "Your AI video from AnyTutor is ready!"
    body = f"""Hi {name}! Your video is ready for download as an attachment.\n\nIf you have any feedback or suggestions, do drop us an email at this email address! :)
            """
    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename=deepfake.mp4",
    )

    text = configure_message(sender_email, receiver_email, subject, body, part)
    return text


def craft_error_email(sender_email, receiver_email, name):
    subject = "Sorry! Your video file could not be generated :("
    body = f"""Hi {name}! We are unable to generate your video file as the files might not have been uploaded correctly.\n\n If you require support please drop us an email at anytutor.official@gmail.com. Thank you! :)
            """
    text = configure_message(sender_email, receiver_email, subject, body)
    return text


def configure_message(sender_email, receiver_email, subject, body, part=False):
    # * Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    if part:
        message.attach(part)    # Add attachment to message

    text = message.as_string()  # Convert message to string
    return text


def send_email(is_lesson=False, error=False):
    # * Set up email details
    port = 465    # For SSL
    with open('config.json', 'r') as f:
        config = json.load(f)
    password = config['ANYTUTOR_GMAIL_PASSWORD']
    sender_email = "anytutor.official@gmail.com"

    # Email filepath depends on where the script is being run from
    with open('email.txt') as f:
        receiver_email = f.readline().strip('\n')

    name = receiver_email.split('@')[0]
    filename = "results/result_lesson.mp4" if is_lesson else "results/result_voice.mp4"

    # * Craft email message
    if error or not os.path.exists(filename):
        text = craft_error_email(sender_email, receiver_email, name)
    else:
        text = craft_email(sender_email, receiver_email, name, filename)

    # * Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

    print("EMAIL SENT")


# Try out send_video_email() if called from command line
if __name__ == "__main__":
    send_email()
    # send_email(is_lesson=True)
    # send_email(error=True)
    # send_email(is_lesson=True, error=True)

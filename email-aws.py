import smtplib, ssl, os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


with open('email.txt') as f:
    receiver_email = f.readline().strip('\n')
    
port = 465    # For SSL
password = "Poignant?"
sender_email = "anytutor.official@gmail.com"
print(receiver_email)
name = receiver_email.split('@')[0]
filename = "results/result_voice.mp4"  # In same directory as script

# Create a multipart message and set headers
message = MIMEMultipart()

if not os.path.isfile(filename):
    subject = "Sorry! Your video file could not be generated :("
    body = f"""Hi {name}! We are unable to generate your video file as the files might not have been uploaded correctly.\n\nIf you require support please drop us an email at anytutor.official@gmail.com. Thank you! :)
    """
else:
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

    # Add attachment to message and convert message to string
    message.attach(part)
    
    
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
# message["Bcc"] = receiver_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))


text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)

print("DONE")

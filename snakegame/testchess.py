import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email credentials
your_email = "vuminhkhang009@gmail.com"
your_password = "Lukelan83"  # Use an app-specific password if you have 2FA enabled

# Email details
to_email = "minhphuongnguyen576@gmail.com"
subject = "Hello from Python"
body = "This is a test email sent from a Python script."

# Create message container
msg = MIMEMultipart()
msg['From'] = your_email
msg['To'] = to_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

# Create SMTP session
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)  # use Gmail with TLS
    server.starttls()  # enable security
    server.login(your_email, your_password)  # login with email and password
    server.sendmail(your_email, to_email, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    server.quit()
import subprocess
import smtplib
import ssl
import random
from email.message import EmailMessage

EMAIL_SENDER = "65050197@kmitl.ac.th"
EMAIL_PASSWORD = "bgph nzay xhka rtbq"
EMAIL_RECEIVER = "channo10mz@gmail.com"

otp = str(random.randint(100000, 999999))

msg = EmailMessage()
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECEIVER
msg["Subject"] = "OTP for Reset"
msg.set_content(f"Your OTP: {otp}")

context = ssl.create_default_context()
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls(context=context)
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.send_message(msg)

user_input = input("Enter OTP to continue reset: ").strip()
if user_input == otp:
    subprocess.run("systemreset.exe", shell=True)
else:
    print("Invalid OTP. Reset blocked.")

import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

valid = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def valid_email(email):
  if(re.fullmatch(valid, email)):
    return True
  else:
    return False

def main(recipient, code):
  message = MIMEMultipart("alternative")
  message["Subject"] = "Barbarian Rising Verification Code"
  message["From"] = "barbrising@gmail.com"
  message["To"] = recipient
  text = f"""Here is your validation code for Barbarian Rising: {code}"""
  sender = "barbrising@gmail.com"
  
  with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
      server.login("barbrising@gmail.com", "xvkm preg ozid gipx")
      messageText = MIMEText(text, "plain")
      message.attach(messageText)
      server.sendmail(
          sender,
          [recipient],
          message.as_string()
      )
      print("Email sent sucessfully. Check email.")

if __name__ == '__main__':
  main(recipient="jlee4889@gmail.com", code=None)
  
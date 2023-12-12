import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

sender = "andy.azskill@gmail.com"

class EmailSender:
    
    def __init__(self, subject,  recipient):
        self.subject = subject
        self.sender = sender
        self.recipient = recipient
        
    def send(self, content):
        message = MIMEMultipart()
        message["subject"] = self.subject
        message["from"] = self.sender
        message["to"] = self.recipient
        message.attach(MIMEText(content,"html"))
        
        try:
            with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
                smtp.ehlo()
                smtp.starttls() 
                smtp.login(self.sender, "hulu qgoq zoet xkre")
                smtp.send_message(message)
            st.write("已發送")
        except Exception as e:
            st.write("錯誤: ", e)

    
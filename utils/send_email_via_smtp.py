import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
load_dotenv()

SENDER_EMAIL=os.getenv('SENDER_EMAIL',"")
SENDER_EMAIL_PASSWORD=os.getenv('SENDER_EMAIL_PASSWORD',"")

def send_smtp_email(user_email,otp,specific_html_content):
    msg=EmailMessage()
    msg['SUBJECT']="Verify your account"
    msg['FROM']=SENDER_EMAIL
    msg['TO']=user_email
    msg.set_content(f"""Your verification code: {otp}
                    This OTP is valid for 5 minutes. Please do not share it with anyone.
                    Best Regards,
                    Panku IT Services
                    NIT PATNA
                    """)
    
    html_content = specific_html_content
    msg.add_alternative(html_content,subtype="html")
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
            smtp.login(SENDER_EMAIL,SENDER_EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Error during sendin email process:",e)
        return False
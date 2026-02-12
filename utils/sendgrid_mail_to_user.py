import os
from dotenv import load_dotenv
load_dotenv()
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDER_EMAIL=os.getenv('SENDER_EMAIL','')
SENDGRID_API_KEY=os.getenv('SENDGRID_API_KEY')

def sendgrid_mail_to_user(user_email,otp):
    print("from sendgrif fun:")
    messege=Mail(
        from_email=SENDER_EMAIL,
        to_emails=user_email,
        subject="Verify your account",
        html_content = f"""
              <div style="font-family: Arial, sans-serif; border: 1px solid #eee; padding: 20px; border-radius: 10px;">
                      <h2 style="color: #333;">Account Verification Code</h2>
                      <p>Hello,</p>
                      <p>Thank you for signing up with us. Please use the following OTP (One-Time Password) code to verify your account:</p>
                      <div style="background: #f4f4f4; padding: 10px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 5px; color: #007bff;">
                          {otp}
                      </div>
                      <p>This OTP is valid only for 5 minutes. Please do not share it with anyone.</p>
                      <br>
                      <p>Best Regards,<br>Panku IT Services,<br>From NIT Patna</p>
                      <p style="margin: 5px 0 0 0; font-size: 12px; color: #95a5a6;">Ayodhya, Uttar Pradesh, India | support@pankajjnv2005@gmail.com</p>
              </div>
             """
    )

    try:
        print("from send  grid try block")
        sendgrid_client=SendGridAPIClient(SENDGRID_API_KEY)
        sendgrid_client.send(messege)
        return True
    except Exception as e:
        print(f"Error occured: {e}")
        return False
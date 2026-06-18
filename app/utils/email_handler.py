import resend
from app.config import settings

resend.api_key = settings.RESEND_API_KEY

def send_otp_email(to_email: str, otp: str):
    try:
        params = {
            "from": "Finance Tracker <tanishqsonawane2318@gmail.com>",  # use your verified domain later
            "to": [to_email],
            "subject": "Your OTP Code",
            "html": f"<p>Your OTP is: <strong>{otp}</strong>. It expires in 10 minutes.</p>"
        }
        email = resend.Emails.send(params)
        return email
    except Exception as e:
        raise Exception(f"Email send failed: {str(e)}")
def send_otp_email(to_email: str, otp: str):
    try:
        params = {
            "from": "Finance Tracker <onboarding@resend.dev>",
            "to": [to_email],
            "subject": "Your OTP Code",
            "html": f"<p>Your OTP is: <strong>{otp}</strong>. It expires in 10 minutes.</p>"
        }
        email = resend.Emails.send(params)
        print(f"Resend response: {email}")  # ADD THIS
        return email
    except Exception as e:
        print(f"Resend error: {str(e)}")  # ADD THIS
        raise Exception(f"Email send failed: {str(e)}")
import resend
from ..config import settings

resend.api_key = settings.RESEND_API_KEY

def send_otp_email(to_email: str, otp: str):
    resend.Emails.send({
        "from": "Finance Tracker <onboarding@resend.dev>",
        "to": to_email,
        "subject": "Your Finance Tracker OTP",
        "html": f"""
        <html><body style="font-family:sans-serif;background:#f5f5f5;padding:40px">
          <div style="max-width:400px;margin:auto;background:white;border-radius:12px;padding:32px">
            <h2 style="color:#6366f1;margin:0 0 8px">Finance Tracker</h2>
            <p style="color:#666;margin:0 0 24px">Your one-time password</p>
            <div style="background:#f0f0ff;border-radius:8px;padding:20px;text-align:center">
              <span style="font-size:36px;font-weight:700;letter-spacing:8px;color:#6366f1">{otp}</span>
            </div>
            <p style="color:#999;font-size:13px;margin:20px 0 0">
              Expires in 5 minutes. Do not share this OTP.
            </p>
          </div>
        </body></html>
        """
    })
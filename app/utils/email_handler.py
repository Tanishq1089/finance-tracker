import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..config import settings

def send_otp_email(to_email: str, otp: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Finance Tracker OTP"
    msg["From"] = settings.MAIL_FROM
    msg["To"] = to_email

    html = f"""
    <html><body style="font-family:sans-serif;background:#f5f5f5;padding:40px">
      <div style="max-width:400px;margin:auto;background:white;border-radius:12px;padding:32px">
        <h2 style="color:#6366f1;margin:0 0 8px">Finance Tracker</h2>
        <p style="color:#666;margin:0 0 24px">Your one-time password</p>
        <div style="background:#f0f0ff;border-radius:8px;padding:20px;text-align:center">
          <span style="font-size:36px;font-weight:700;letter-spacing:8px;color:#6366f1">{otp}</span>
        </div>
        <p style="color:#999;font-size:13px;margin:20px 0 0">Expires in 5 minutes. Do not share this OTP.</p>
      </div>
    </body></html>
    """
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
        server.starttls()
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        server.sendmail(settings.MAIL_FROM, to_email, msg.as_string())
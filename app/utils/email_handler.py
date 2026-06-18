import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_otp_email(to_email: str, otp: str):
    subject = "Your Finance Tracker OTP"

    html = f"""
    <html>
    <body style="font-family:sans-serif;background:#f5f5f5;padding:40px">
      <div style="max-width:400px;margin:auto;background:white;border-radius:12px;padding:32px">
        <h2 style="color:#6366f1">Finance Tracker</h2>

        <p>Your one-time password:</p>

        <div style="background:#f0f0ff;border-radius:8px;padding:20px;text-align:center">
          <span style="font-size:36px;font-weight:700;letter-spacing:8px;color:#6366f1">
            {otp}
          </span>
        </div>

        <p style="color:#999;font-size:13px;margin-top:20px">
          Expires in 5 minutes. Do not share this OTP.
        </p>
      </div>
    </body>
    </html>
    """

    print("========== EMAIL DEBUG ==========")
    print("EMAIL_USER =", EMAIL_USER)
    print("EMAIL_PASSWORD EXISTS =", EMAIL_PASSWORD is not None)
    print("Sending OTP to =", to_email)

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(html, "html"))

    try:
        print("Connecting to Gmail SMTP...")

        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)

        print("Starting TLS...")
        server.starttls()

        print("Logging in...")
        server.login(EMAIL_USER, EMAIL_PASSWORD)

        print("Sending email...")
        server.send_message(msg)

        print("Email sent successfully!")

        server.quit()

    except Exception as e:
        print("SMTP ERROR:", str(e))
        raise
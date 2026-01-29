import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()
mcp = FastMCP("EmailMCPServer")

# Default SMTP settings (can be overridden via environment variables or tool parameters)
# These are the original default values - users can override via env vars or tool parameters
DEFAULT_SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
DEFAULT_SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
DEFAULT_SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
DEFAULT_SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")


@mcp.tool
def send_email(
    sender: str,
    recipient: str,
    subject: str,
    body: str,
    smtp_server: str = None,
    smtp_port: int = None,
    smtp_username: str = None,
    smtp_password: str = None
) -> bool:
    """
    Send an email using SMTP.
    
    Args:
        sender: Email address of the sender
        recipient: Email address of the recipient
        subject: Email subject
        body: Email body content
        smtp_server: SMTP server address (defaults to SMTP_SERVER env var or smtp.gmail.com)
        smtp_port: SMTP server port (defaults to SMTP_PORT env var or 465)
        smtp_username: SMTP username/email (defaults to SMTP_USERNAME env var)
        smtp_password: SMTP password/app password (defaults to SMTP_PASSWORD env var)
    
    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        # Use provided credentials or fall back to defaults/environment variables
        server = smtp_server or DEFAULT_SMTP_SERVER
        port = smtp_port or DEFAULT_SMTP_PORT
        username = smtp_username or DEFAULT_SMTP_USERNAME
        password = smtp_password or DEFAULT_SMTP_PASSWORD
        
        # Note: Default credentials are used if not provided
        # Users can override by providing smtp_username/smtp_password parameters
        # or by setting SMTP_USERNAME/SMTP_PASSWORD environment variables
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to SMTP server
        # Port 465 uses SSL/TLS directly, port 587 uses STARTTLS
        if port == 465:
            with smtplib.SMTP_SSL(server, port) as smtp_server:
                smtp_server.login(username, password)
                smtp_server.sendmail(sender, recipient, msg.as_string())
        elif port == 587:
            with smtplib.SMTP(server, port) as smtp_server:
                smtp_server.starttls()
                smtp_server.login(username, password)
                smtp_server.sendmail(sender, recipient, msg.as_string())
        else:
            # Try SSL first, fallback to STARTTLS
            try:
                with smtplib.SMTP_SSL(server, port) as smtp_server:
                    smtp_server.login(username, password)
                    smtp_server.sendmail(sender, recipient, msg.as_string())
            except:
                with smtplib.SMTP(server, port) as smtp_server:
                    smtp_server.starttls()
                    smtp_server.login(username, password)
                    smtp_server.sendmail(sender, recipient, msg.as_string())
        
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)

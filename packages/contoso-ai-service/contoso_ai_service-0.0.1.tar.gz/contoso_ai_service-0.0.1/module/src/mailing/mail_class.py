import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from concurrent.futures import ThreadPoolExecutor
import os
from dotenv import load_dotenv


# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")
load_dotenv(dotenv_path)


class Mailer:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", "SMTP_PORT"))
        self.sender_email = os.getenv("SENDER_EMAIL", "SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD", "SENDER_PASSWORD")



    def connect_to_server(self):
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            return server

        except Exception as e:
            print(f"Error connecting to the server: {e}")
            return None

    def send_text_email(
        self, to_email, subject, body, cc=None, bcc=None, attachments=None
    ):
        """
        Send a text email.

        Parameters:
        - to_email (str): Recipient email address.
        - subject (str): Email subject.
        - body (str): Email body content.
        - cc (list): List of email addresses to be CC'd.
        - bcc (list): List of email addresses to be BCC'd.
        - attachments (list): List of file paths for email attachments.

        Example:
        swift_sender.send_text_email(
            to_email="recipient@example.com",
            subject="Subject",
            body="Hello, this is a text email.",
            cc=["cc@example.com"],
            bcc=["bcc@example.com"],
            attachments=["/path/to/file1.txt", "/path/to/file2.pdf"]
        )
        """

        server = self.connect_to_server()
        if server:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = to_email
            message["Subject"] = subject

            if cc:
                message["Cc"] = ", ".join(cc)
            if bcc:
                message["Bcc"] = ", ".join(bcc)

            message.attach(MIMEText(body, "plain"))

            server.sendmail(self.sender_email, to_email, message.as_string())
            server.quit()




    def send_html_email(
        self, to_email, subject, body, cc=None, bcc=None, attachments=None
    ):
        server = self.connect_to_server()
        if server:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = to_email
            message["Subject"] = subject

            if cc:
                message["Cc"] = ", ".join(cc)
            if bcc:
                message["Bcc"] = ", ".join(bcc)

            message.attach(MIMEText(body, "html"))

            server.sendmail(self.sender_email, to_email, message.as_string())
            server.quit()




    def send_multiple_emails(self, recipients, subject, body, is_html=False):
        with ThreadPoolExecutor() as executor:
            if is_html:
                executor.map(
                    lambda recipient: self.send_html_email(recipient, subject, body),
                    recipients,
                )
            else:
                executor.map(
                    lambda recipient: self.send_text_email(recipient, subject, body),
                    recipients,
                )





    def attach_file_to_message(self, message, file_path):
        """
        Attach a file to the email message.

        Parameters:
        - message (MIMEMultipart): Email message.
        - file_path (str): Path to the file to be attached.
        """
        from email.mime.application import MIMEApplication
        from email import encoders

        with open(file_path, "rb") as file:
            attachment = MIMEApplication(file.read(), Name=os.path.basename(file_path))
            attachment[
                "Content-Disposition"
            ] = f"attachment; filename={os.path.basename(file_path)}"
            message.attach(attachment)

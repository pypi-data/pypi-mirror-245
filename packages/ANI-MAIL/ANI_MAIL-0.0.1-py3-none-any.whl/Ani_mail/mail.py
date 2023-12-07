import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
from email.header import decode_header



class main:

    def send_email(email_address, email_password, recipient_email, subject, body):
        message = MIMEMultipart()
        message["From"] = email_address
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_address, email_password)
            server.sendmail(email_address, recipient_email, message.as_string())
            print("Email has been sent.")


    def check_new_emails(email_address, email_password, number_of_mails):
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        mail.login(email_address, email_password)
        mail.select("inbox")
        result, data = mail.search(None, "UNSEEN")
        email_ids = data[0].split()
        print(f"Number of new emails: {len(email_ids)}")
        for i in range(min(number_of_mails, len(email_ids))):
            result, msg_data = mail.fetch(email_ids[i], "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            from_ = msg.get("From")
            print(f"\nEmail {i + 1}:")
            print(f"Subject: {subject}")
            print(f"From: {from_}")
        mail.logout()


    def clear_inbox(email_address, email_password):
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        mail.login(email_address, email_password)
        mail.select("inbox")
        result, data = mail.search(None, "ALL")
        if result == "OK":
            for num in data[0].split():
                mail.store(num , '+FLAGS', '(\Deleted)')
            mail.expunge()
        mail.logout()



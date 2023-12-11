import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
from email.header import decode_header
from time import sleep


class Email_Manager:

    def send_email(email_address, email_password, recipient_email, subject, message):
        try:
            msg = MIMEMultipart()
            msg["From"] = email_address
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(email_address, email_password)
                server.sendmail(email_address, recipient_email, msg.as_string())
                print("Email has been sent.")
        except Exception as e:
            print(e)


    def send_bulk_email(email_address, email_password, recipient_emails, subject, message):
        try:
            for recipient_email in recipient_emails:
                msg = MIMEMultipart()
                msg["From"] = email_address
                msg["To"] = recipient_email
                msg["Subject"] = subject
                msg.attach(MIMEText(message, "plain"))
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(email_address, email_password)
                    server.sendmail(email_address, recipient_email, msg.as_string())
                    print("Email has been sent to {}".format(recipient_email))
        except Exception as e:
            print(e)


    def check_new_emails(email_address, email_password, number_of_mails):
        try:
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
        except Exception as e:
            print(e)


    def clear_inbox(email_address, email_password):
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
            mail.login(email_address, email_password)
            mail.select("inbox")
            result, data = mail.search(None, "ALL")
            if result == "OK":
                for num in data[0].split():
                    mail.store(num , '+FLAGS', '(\Deleted)')
                mail.expunge()
            mail.logout()
        except Exception as e:
            print(e)


    def clear_email_trash(email_address, email_password):
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(email_address, email_password)
            mail.select("[Gmail]/Trash")
            result, data = mail.search(None, "ALL")
            if result == "OK":
                for num in data[0].split():
                    mail.store(num , '+FLAGS', '(\Deleted)')
                mail.expunge()
                print("Trash box cleared successfully.")
            else:
                print("Error while fetching emails from the Trash box.")
            mail.logout()
        except Exception as e:
            print(e)


    def email_bombing(email_address, email_password, recipient_email, subject, message, count_of_mails, wait_time):
        try:
            msg = MIMEMultipart()
            msg["From"] = email_address
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))
            count = 1
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(email_address, email_password)
                for i in range(int(count_of_mails)):
                    server.sendmail(email_address, recipient_email, msg.as_string())
                    print("Email has been sent {}".format(count))
                    count += 1
                    sleep(int(wait_time))
        except Exception as e:
            print(e)





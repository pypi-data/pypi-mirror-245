#ANI_MAIL

A Python package to send mail, read mail and clear inbox.

#HOW TO USE IT

from Ani_mail import mail

mail.main.send_email(email_address, email_password, recipient_email, subject, body)

mail.main.check_new_emails(email_address, email_password, number_of_mails)

mail.main.clear_inbox(email_address, email_password)


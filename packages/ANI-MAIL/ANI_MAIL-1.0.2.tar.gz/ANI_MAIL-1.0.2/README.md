# ANI_MAIL

A Python package created by Aniket Dubey for send mail, bulk mail, read new received mail, clear inbox and clear trash box.

Also you can mail bombing using this


## HOW TO USE IT
from Ani_EmailManager import EmailManager

## For sending emails
EmailManager.Email_Manager.send_email(email_address, email_password, recipient_email, subject, message)

## For sending emails to many mail IDs
EmailManager.Email_Manager.send_bulk_email(email_address, email_password, recipient_emails, subject, message)

## For getting new received mails, also you can set count of mails you wanna get.
EmailManager.Email_Manager.check_new_emails(email_address, email_password, number_of_mails)

## For clearing your whole inbox
EmailManager.Email_Manager.clear_inbox(email_address, email_password)

## For clearing your whole trash box
EmailManager.Email_Manager.clear_email_trash(email_address, email_password)

## For email bombing
EmailManager.Email_Manager.email_bombing(email_address, email_password, recipient_email, subject, message, count_of_mails, wait_time)

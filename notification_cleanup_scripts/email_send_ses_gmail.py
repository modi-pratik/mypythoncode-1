# need to install boto : pip install boto
import boto
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from sos.plugins.sendmail import sendmail
import email
import smtplib


# SES email using boto lib
def send_ses(fromaddr,
             subject,
             body,
             recipient,
             attachment=None,
             filename=''):
    """Send an email via the Amazon SES service.

    Example:
      send_ses('me@example.com, 'greetings', "Hi!", 'you@example.com)

    Return:
      If 'ErrorResponse' appears in the return message from SES,
      return the message, otherwise return an empty '' string.
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = recipient
    msg.attach(MIMEText(body))
    if attachment:
        part = MIMEApplication(attachment)
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(part)
    mail_user, mail_pwd = 'AKIAID5RG3NYEUOUGVCA', 'AguMqTOnsqejVEgBAdzLOjVtfJIKWGX6EM2i5sSrOrWL'
    conn = boto.connect_ses(mail_user, mail_pwd)
    result = conn.send_email(msg.as_string())
    return result if 'ErrorResponse' in result else ''


# email send using gmail
def send_mail_gmail(mail_from, mail_to, host, message, mail_user, mail_pwd):
    FROM = mail_from
    TO = mail_to

    TEXT = message
    msg = email.MIMEMultipart.MIMEMultipart()
    msg['From'] = mail_from
    msg['To'] = TO
    msg['Subject'] = "Script Output for workmob notifications"
    msg.attach(MIMEText(TEXT))

    try:
        server = smtplib.SMTP(host, 587)
        server.ehlo()
        server.starttls()

        server.login(mail_user, mail_pwd)
        server.sendmail(FROM, TO, msg.as_string())
        #server.quit()
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"


# SES email send simple, using only smtplib
def send_email_amazon_ses(mail_from, mail_to, message):
    fromaddr = mail_from
    toaddrs = mail_to
    # print "Message length is " + repr(len(message))

    msg = email.MIMEMultipart.MIMEMultipart()
    msg['From'] = mail_from
    msg['To'] = ', '.join(mail_to)
    msg['Subject'] = "Script Output for workmob notifications"
    msg.attach(MIMEText(message))

    #Change according to your settings
    smtp_server = 'email-smtp.us-east-1.amazonaws.com'

    mail_user, mail_pwd = 'AKIAID5RG3NYEUOUGVCA', 'AguMqTOnsqejVEgBAdzLOjVtfJIKWGX6EM2i5sSrOrWL'

    smtp_username = mail_user
    smtp_password = mail_pwd
    smtp_port = '587'
    smtp_do_tls = True

    server = smtplib.SMTP(
        host=smtp_server,
        port=smtp_port,
        timeout=10
    )

    server.set_debuglevel(10)
    server.starttls()
    server.ehlo()
    server.login(smtp_username, smtp_password)
    for to_email in toaddrs:
        server.sendmail(fromaddr, to_email, msg.as_string())
    print server.quit()

#  Following are testing for all functions here
# send_email_amazon_ses(mail_from='hello@workmobmail.com',
#                       mail_to=['snehal@arcgate.com', 'manish@arcgate.com'], message='test mail')

# send_ses('hello@workmobmail.com', 'test mail', 'body of mail', 'snehal@arcgate.com')

# send_mail_gmail(mail_from='arcgatemailtest@gmail.com', mail_to='snehaldot@gmail.com',
#                 host='smtp.gmail.com', message='TEXT', mail_user='arcgatemailtest@gmail.com', mail_pwd='Arcgate1!')
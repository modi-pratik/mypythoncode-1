import smtplib
import pika
import time
import datetime
import json
import sys


# fromaddr = 'snehal.java@gmail.com'
# toaddrs  = 'snehaldot@gmail.com'
# msg = 'There was a terrible error that occured and I wanted you to know!'
#
#
# # Credentials (if needed)
# username = 'snehal.java@gmail.com'
# password = 'snehaldot@12'
#
# # The actual mail send
# server = smtplib.SMTP('smtp.gmail.com:587')
# server.ehlo()
# server.starttls()
# server.login(username, password)
# server.sendmail(fromaddr, toaddrs, msg)
# server.quit()


# class Mail():
#     mail_from = ''
#     mail_to = ''
#     mail_body = ''
#
#     def __init__(self):
#         mail_from = self.mail_from
#         mal_to = self.mail_to
#         mail_body = self.mail_body


def send_email(mail_from, mail_to, mail_body):
    gmail_user = "snehal.java@gmail.com"
    gmail_pwd = "snehaldot@12"
    FROM = mail_from
    TO = [mail_to] #must be a list
    SUBJECT = "Testing sending using gmail"
    TEXT = """From: From Person <from@fromdomain.com>
              To: To Person <to@todomain.com>
              MIME-Version: 1.0
              Content-type: text/html
              Subject: SMTP HTML e-mail test

              This is an e-mail message to be sent in HTML format

              <b>This is HTML message.</b>
              <h1>This is headline.</h1>
              """

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        #server = smtplib.SMTP(SERVER)
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        #server.quit()
        server.close()
        print 'successfully sent the mail'
        return 0
    except:
        print "failed to send mail"
        return 1

if __name__ == '__main__':
    send_email()

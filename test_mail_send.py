#!/usr/bin/python
import smtplib


# def prompt(prompt):
#     return raw_input(prompt).strip()

fromaddr = 'hello@workmobmail.com'
toaddrs  = 'snehal@arcgate.com'
msg = """From: hello@workmobmail.com

Hello, this is dog.
"""

print "Message length is " + repr(len(msg))

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
# import ipdb
# ipdb.set_trace()
server.sendmail(fromaddr, toaddrs, msg)
print server.quit()



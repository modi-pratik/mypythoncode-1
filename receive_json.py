#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import smtplib
import pika
import time
import datetime
import json
# import sys
from send_mail import send_email


max_retries = 3
queue = 'retries'

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue=queue, durable=True)

print '[*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    data = json.loads(body)

    print "[>] Received '%s' (try: %d)" % (data.get('mail_from'), 1 + int(properties.priority))

    if properties.priority >= max_retries - 1: # example handling retries
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print "[!] '%s' rejected after %d retries" % (data.get('mail_from'), 1 + int(properties.priority))
    else:
        try:
            mail_from = data.get("mail_from")
            mail_to = data.get("mail_to")
            mail_body = data.get("mail_body")
            # print "data :", data
            res = send_email(mail_from, mail_to, mail_body)
            if res:
                print "Error in sending mail"
            else:
                # update record entry for mail sent
                print "Mail sent"

            # time.sleep(len(data.get('keyword')))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print "[+] Done"

        except:
            print "Exception in sending mail from queue"


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()
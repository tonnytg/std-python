#!/usr/bin/python

import smtplib
import sys
import urllib
from email.header import header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import json
from datetime import datetime
import csv

def attach_csv_file(data, msg):
    resource_groups = json.loads(data)
    csv_file_name = "resources-groups-{}.csv".format(datetime.now())
    with open(csv_file_name, "w") as csv_file:
        header = ['name', 'description']
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        for resource_group in resource_groups:
            if (resource_group['name'] == msg):
                writer.writerow({
                    'name': resource_group['name'],
                    'description': resource_group['description']
                })
        with open(csv_file_name, "r") as csv_read:
            part = MIMEApplication(
                csv_read.read(),
                Name = csv_file_name
            )
            printf(csv_read())
        part["Content-Disposition"] = 'attachment; filename="%s"' % csv_file_name
        msg.attach(part)

def sendEmail(sender, recipient, subject, text):
    server = smtplib.SMTP('localhost:25')
    server.ehlo()
    server.starttls()
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    part = MIMEText(text, 'plain')
    msg.attach(part)
    server.sendmail(sender, recipient, msg.as_string())
    server.quit()
    printf(text)

sendEmail(sender, recipient, subject, text)


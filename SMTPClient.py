
import sys
import os
import re

import smtplib

class SMTPClient:

	def __init__(self):
		pass

	def send_email(self, recipient, dimension):
	    gmail_user = 'ramseyrikk@gmail.com'
	    gmail_pwd = 'bangiversary'
	    FROM = gmail_user
	    TO = recipient if type(recipient) is list else [recipient]
	    SUBJECT = 'Cloud and clear'
	    TEXT = "Found a new counter example of size %d" %dimension

	    # Prepare actual message
	    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
	    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
	    try:
	        server = smtplib.SMTP("smtp.gmail.com", 587)
	        server.ehlo()
	        server.starttls()
	        server.login(gmail_user, gmail_pwd)
	        server.sendmail(FROM, TO, message)
	        server.close()
	        print 'successfully sent the mail'
	    except:
	        print "failed to send mail"

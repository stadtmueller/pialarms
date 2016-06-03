#! /usr/bin/env python
# -*- coding: utf8 -*-
# FILENAME: Mail.py

import os
import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBASE import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email import Encoders

class Email( object ):
    self.recipient = ""
    self.smtpserver = "smtp.googlemail.com"
    self.username = ""
    self.password = ""
    self.filename = ""

    def send( self ):
        mail = MIMEMultipart()
        mail[ "From"    ] = "pialarms"
        mail[ "To"      ] = self.recipient
        mail[ "Date"    ] = formadate( localtime=True )
        mail[ "Subject" ] = "Movement detected"

        mail.attach( MIMEText( "" ) )

        att = MIMEBase( "application", "octet-stream" )
        att.set_payload( open( self.filename, "rb" ).read() )
        Encoders.encode_base64( att )
        att.add_header( "Content-Disposition", 'attachment; filename="%s"' % os.path.basename( self.filename ) )

        mail.attach( att )

        server = smtplib.SMTP( self.smtpserver )
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login( self.username, self.password )
        server.sendmail( "pialarms", self.recipient, mail.as_string() )
        server.quit()

    def setFile( filename ):
        self.filename = filename

    def setLoginData( recepient, username, password ):
        self.recipient = recipient
        self.username = username
        self.password = password


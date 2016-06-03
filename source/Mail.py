# This file is part of PiAlarms.
#
#    PiAlarms is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PiAlarms is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PiAlarms.  If not, see <http://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------

#! /usr/bin/env python
# -*- coding: utf8 -*-
# FILENAME: Mail.py

import os
import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email import Encoders

class Email( object ):
    recipient = ""
    smtpserver = "smtp.googlemail.com"
    username = ""
    password = ""
    filename = ""

    def send( self ):
        mail = MIMEMultipart()
        mail[ "From"    ] = "pialarms"
        mail[ "To"      ] = self.recipient
        mail[ "Date"    ] = formatdate( localtime=True )
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

    def setFile( self, filename ):
        if os.path.isfile( filename ):
            self.filename = filename
        else:
            print( filename + " is not a valid file. Choose a different." )

    def setLoginData( self, recipient, username, password ):
        self.recipient = recipient
        self.username = username
        self.password = password


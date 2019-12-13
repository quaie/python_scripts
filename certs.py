#!/usr/bin/env python

import commands
import subprocess
from OpenSSL import crypto
import smtplib

_list = []

f=open("./orma", "r")

for i in f:
  #print(i)
  command = 'ldapsearch -D "cn=reader,ou=Local,o=org,c=COM" -o ldif-wrap=no -LL -t -x -T /tmp/ -H ldaps://ldap.example.COM:636/ -b "o=Admin,c=COM" \'(mail={0})\' 2>/dev
/null | grep userCert | cut -d"<" -f2 | cut -d":" -f2'.format(i.strip())
  if 'tmp' not in commands.getstatusoutput(command)[1]:
    #print commands.getstatusoutput(command)
    #print(i)
    _list.append(i.strip())
  else:
    _file = commands.getstatusoutput(command)[1]
    der_file = open(_file, 'r')
    x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, der_file.read())
    if x509.has_expired():
      _list.append(i.strip())

#print(list(dict.fromkeys(_list)))
_nok_addresses = list(dict.fromkeys(_list))

f.close()

#cleanup at the end
command=('rm -f /tmp/ldapsearch-userCertificatebinary-*')
subprocess.call(command, shell=True)

#now we send the mail, in an archaic manner :)

fromaddr = 'x@x'
toaddrs  = ['x@x']
# string inside msg below must have "Subject: <subject line>\n"
# for a subject to be sent, and "To: " for the recipient to be shown in the email
msg = '''To: x@x
    Subject: server test\n
    the email addresses below don't have their certificate published @ ldap server
    or the certificate has expired
    \n
    server cannot send emails to the addresses listed below.
    please forward the email to:
    - x@x
    - x@x
    \n\n
'''

msg = (msg + str(_nok_addresses)).format(fromaddr =fromaddr, toaddr = toaddrs[0])
# The actual mail send
server = smtplib.SMTP('server:25')
#server.starttls()
server.ehlo("example.com")
server.mail(fromaddr)
server.rcpt(toaddrs[0])
server.data(msg)
server.quit()

# Right now it won't download same file name twice even if their contents are different.

import email
import getpass, imaplib
import os
import sys

f = open('parsedmail_raw.txt','w')  #outputs file as parsedmail_raw.txt
detach_dir = '.'
if 'attachments' not in os.listdir(detach_dir):
    os.mkdir('attachments')

userName = raw_input('Username: ')
passwd = getpass.getpass('Password: ')
imap_server = '<IMAP SERVER>'  #Enter your imap server here
mailbox_folder = 'Inbox/Spam'  #Change folder as needed
msgCount = 1
try:
    imapSession = imaplib.IMAP4_SSL(imap_server, 993)
    print 'Connecting to %s' % imap_server
    typ, accountDetails = imapSession.login(userName, passwd)
    if typ != 'OK':
        print 'Not able to sign in!'
        raise

    imapSession.select(mailbox_folder)
    typ, data = imapSession.search(None, 'ALL')
    print 'Using %s as mailbox' % mailbox_folder
    if typ != 'OK':
        print 'Error searching Inbox.'
        raise

    # Iterating over all emails
    for msgId in reversed(data[0].split()):
        typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
        if typ != 'OK':
            print 'Error fetching mail.'
            raise

        emailBody = messageParts[0][1]
        mail = email.message_from_string(emailBody)
        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                # print part.as_string()
				print "Message Number %s" % msgCount
				print 'From: ', mail['From']
				print 'To: ', mail['To']
				print 'Subject: ', mail['Subject']
				print 'Date:', mail['Date']
				for id in mail.get_all("Message-ID") : 
					print "Message-ID: {0}".format(id)
				print '\n'
				f.write("Message Number: %s\n" % msgCount)
				f.write("%s\n" % emailBody)
				#f.write("%s" % mail.get_payload)
				msgCount += 1
				continue

            fileName = part.get_filename()
            #print 'Attachment: %s' % fileName
			# uncomment if you want to download attachments
            if bool(fileName):
                filePath = os.path.join(detach_dir, 'attachments', fileName)
                if not os.path.isfile(filePath) :
                    print 'Downloading file: %s' % fileName
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
    imapSession.close()
    imapSession.logout()
except :
    print 'Not able to download all attachments.'

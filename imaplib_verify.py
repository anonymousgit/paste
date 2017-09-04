import imaplib
import email
import os

msgid = '2017049065048.2131CD9D02@mail.anonymous744wjcx.onion'
imap = imaplib.IMAP4_SSL('anonymous744wjcx.onion')
imap.login('lists@anonymous744wjcx.onion', 'lists')
imap.select('lists.bsd-talk.2017.04', True)

typ, data = imap.uid('search', None, '(HEADER Message-Id {})'.format(msgid))
for uid in data[0].split():
	typ, data = imap.uid('fetch', uid, '(RFC822)')
	message = email.message_from_bytes(data[0][1])
	if message.get_content_type() == "multipart/signed":
		with open("msg", "wb") as msg:
			msg.write(message.get_payload(0).as_bytes())
		with open("sig", "wb") as sig:
			sig.write(message.get_payload(1).as_bytes())
		os.execvp("gpg", ["gpg", "--verify", "sig", "msg"])

imap.close()
imap.logout()

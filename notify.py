import mailtools
from mailtools import SMTPMailer


def send_email(video_notice):
  
    mailer = SMTPMailer('127.0.0.1')

    message = unicode(video_notice)

    mailer.send_plain(
        u'test@test.com',
        [u'your@emailYourSendingFrom.com'],
        u'Tennis video expired',
        message
    )


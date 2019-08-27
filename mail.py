#!/usr/bin/env python3
# coding=utf-8
import logging.handlers
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


class Mail(object):
    def __init__(self, text, sender, receiver, subject, logger, smtp_server, from_addr, password):
        self.logger = logger
        self.text = text
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.from_addr = from_addr
        self.smtp_server = smtp_server
        self.password = password
        self.to_addr = self.from_addr
        # From above to below: mail content, sender nickname, receiver nickname, subject
        self.msg = MIMEText(self.text, 'plain', 'utf-8')
        self.msg['From'] = self._format_addr(self.sender + '<' + self.from_addr + '>')
        self.msg['To'] = self._format_addr(self.receiver + '<' + self.to_addr + '>')
        self.msg['Subject'] = Header(self.subject, 'utf-8').encode()

    # format the email address
    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send(self):
        self.logger.info('send mail start!')
        # server = smtplib.SMTP(self.smtp_server, 25)  # 25 normal，465 SSL
        server = smtplib.SMTP_SSL(self.smtp_server, 465)
        # server.starttls()  # SSL required
        server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, [self.to_addr], self.msg.as_string())
        self.logger.info('----This email\'s info: %s, %s, %s', self.text, self.receiver, self.to_addr)
        server.quit()


if __name__ == '__main__':
    logging.basicConfig(filename='biz.log', format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]',
                        level=logging.DEBUG, filemode='a', datefmt='%Y-%m-%d %I:%M:%S %p')
    send_email = Mail('test', 'wo', 'ni', '仓位变动', 'xxx@qq.com')
    send_email.send()

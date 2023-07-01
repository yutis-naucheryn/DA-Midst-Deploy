from werkzeug.routing import BaseConverter
from flask_mail import Message, Mail
from . import mail

class ListConverter(BaseConverter):

    def to_python(self, value):
        return value.split('+')

    def to_url(self, values):
        return '+'.join(BaseConverter.to_url(value)
                        for value in values)
    
def send_email(recipient, subject, html_content):
    msg = Message(subject, recipients=[recipient])
    msg.html = html_content
    mail.send(msg)
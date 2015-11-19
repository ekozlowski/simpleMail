import mimetypes
import os
import smtplib
import sys

# If we're using python 3
if sys.version_info > (3,):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
else:
    from email.MIMEText import MIMEText
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email import Encoders as encoders

SMTP_SERVER = 'smtp.gmail.com:587'  # default to gmail, you can set this to your home-base SMTP server too. :)
SMTP_USERNAME = 'ekozlowski1@gmail.com' # <-- The Gmail address this message will originate from.
SMTP_PASSWORD = 'qkhemkrmkowxlrlb' # <-- Generate an app password at https://security.google.com/settings/security/apppasswords
DEFAULT_FROM_ADDRESS = 'ekozlowski1@gmail.com' # I set this to my gmail address.  You should set it to the email address you use most often.
                                         # you can override it on the function call, using the frm parameter.
DEFAULT_TO_ADDRESS = 'ekozlowski1@gmail.com' # again, I set this as my gmail address... because I use this for notifications...
DEFAULT_SUBJECT = 'Eds Email Subject!  Woo!' # just a default - can be whatever.
DEFAULT_MESSAGE = 'Eds Default Email Message' # just a default - can be whatever.


def send_email(frm, to, subject, message, attachments=None, maxsize=100000, html=False):
    """
    frm - (string) Email address this message will appear to originate from.
    to - (string, or list of strings) - Email address(es) this message should be sent to.
    subject - (string) Subject of email
    message - (string) Message body of email
    attachments (list) - Paths to attachments to this message
    maxsize (int) - Maximum size (in characters) for this message
    html (bool) - If set to true, the message is sent as HTML.  False (plain text) is the default.
    """
    if attachments is None:
        attachments = []

    # If we've been given max size, truncate the message accordingly.     
    if len(message) > maxsize:
        message = message[:maxsize] + '\n<Rest of message truncated because of size>\n'
    
    m_from = frm
    m_to = to
    msg = MIMEMultipart()

    msg['From'] = m_from
    # if we're passed a string on 'to', don't join with commas.  If we're passed a list,
    # we'll need to join the adddresses with commas.
    if not hasattr(m_to, 'upper'):
        m_to = ','.join(m_to)

    msg['To'] = m_to
    msg['Subject'] = subject
    if html:
        body_msg = MIMEText(message, 'html')
    else:
        body_msg = MIMEText(message)

    msg.attach(body_msg)
    # Attach any attachments we have
    # This will raise an exception if the path isn't there or it is
    # unable to read the file. Attach any kind of file with MIMEBase
    for attachment in attachments:
        mimetype = mimetypes.guess_type(attachment)[0]
        _maintype, _subtype = mimetype.split('/')
        att = MIMEBase(_maintype, _subtype)
        att.set_payload(open(attachment, 'rb').read())
        encoders.encode_base64(att)
        file_name=os.path.basename(attachment)
        att.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(att)

    server = smtplib.SMTP(SMTP_SERVER) 
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    errors = server.sendmail(m_from, m_to, msg.as_string())
    return errors

def send_message(frm=DEFAULT_FROM_ADDRESS, 
                to=DEFAULT_TO_ADDRESS,
                subject=DEFAULT_SUBJECT,
                message=DEFAULT_MESSAGE,
                attachments=None,
                **kwargs):
    return send_email(frm, to, subject, message, attachments)

def send_html_message(frm=DEFAULT_FROM_ADDRESS,
                      to=DEFAULT_TO_ADDRESS,
                      subject=DEFAULT_SUBJECT,
                      message=DEFAULT_MESSAGE,
                      attachments=None):
    return send_email(frm, to, subject, message, attachments, html=True)


if __name__ == "__main__":
    # plain text
    send_message(message='This is a test... this is only a test.')
    
    # HTML
    send_html_message(message="<h1>Hello HTML world!</h1>")

    # with attachment
    send_html_message(message="<h1>Check out this awesome Lynx!", attachments=['./lynx.jpg'])

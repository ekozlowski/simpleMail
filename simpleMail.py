from communicationHelpers.mimes import Mimes

def sendEmail(frm, to, subject, message, attachments=[], **kwargs):
    import os
    import smtplib
    import email.MIMEText 
    import email.MIMEMultipart 
    import email.MIMEBase
    import email.Encoders
    mObj = Mimes()

    # Reduce the max size of the message since we are 
    # allowing attachments now. 
    if len(message) > 100000:
        message = message[:100000] + '\n<Rest of message truncated because of size>\n'
    
    m_from = frm
    m_to = to
    m_to_label = m_to[:] # used in label for email
    msg = email.MIMEMultipart.MIMEMultipart()
    
    msg['From'] = m_from
    msg['To'] = ','.join(m_to_label)
    msg['Subject'] = subject
    if kwargs.get('type'):
        body_msg = email.MIMEText.MIMEText(message, kwargs.get('type'))
    else:
        body_msg = email.MIMEText.MIMEText(message)

    msg.attach(body_msg)
    # Attach any attachments we have
    # This will raise an exception if the path isn't there or it is
    # unable to read the file. Attach any kind of file with MIMEBase
    for attachment in attachments:
        base, ext = mObj.getAsSplit(attachment.split('.')[-1])
        att = email.MIMEBase.MIMEBase(base, ext)
        att.set_payload(open(attachment, 'rb').read())
        email.Encoders.encode_base64(att)
        file_name=os.path.basename(attachment)
        att.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(att)
        
    for name, payload in kwargs.get('mockAttachments', []):
        base, ext = mObj.getAsSplit(name.split('.')[-1])
        att = email.MIMEBase.MIMEBase(base, ext)
        att.set_payload(payload)
        email.Encoders.encode_base64(att)
        att.add_header('Content-Disposition', 'attachment', filename=name)
        msg.attach(att)
        
        
    

    S = smtplib.SMTP('128.103.4.88') 
    errors = S.sendmail(m_from, m_to, msg.as_string())
    return errors

def sendHTMLEmail(frm, to, subject, message, attachments=[], **kwargs):
    return sendEmail(frm, to, subject, message, attachments, type='html', **kwargs)

def sendDefault(to, subject, message,  attachments=[], frm='auto-mail@alcossc.com', **kwargs):
    return sendEmail(frm, to, subject, message, attachments, **kwargs)

def sendDefaultHTML(to, subject, message, attachments=[], frm='auto-mail@alcossc.com', **kwargs):
    return sendEmail(frm, to, subject, message, attachments, type='html', **kwargs)


if __name__ == "__main__":
    sendEmail('noreply@alcossc.com', ['ekozlowski@ALCOStores.com'], 'testMsg','This is a test... this is only a test.', ['C:/eds_example.txt'])
    sendHTMLEmail('noreply@alcossc.com',['ekozlowski@ALCOStores.com'],'testMsg','<html><body>Uh oh! Its html!</body></html>')
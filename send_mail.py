import smtplib
from email.mime.text import MIMEText #Allows us to send text and html emails

def send_mail(customer, dealer, rating, comments):
    # Configurations from Mailtrap.io
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    username #find this from your mailtrap.io first email
    password #find this from your mailtrap.io first email
     

    # Using our imagination
    sender_email = 'email1@example.com'
    receiver_email = 'example2@email.com'

    message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Dealer: {dealer}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"#f-string is a new & improved way to format strings in python

    #The parts of an email
    msg = MIMEText(message, 'html')
    msg['Subject'] = "Lexus Feedback"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Sending the email  
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(username, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
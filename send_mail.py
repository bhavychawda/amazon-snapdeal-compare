import smtplib


def flaskmail(mail,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('add you email here','add you password here')
    server.sendmail('add you email here',mail,content)
    print("mail sent successfully")
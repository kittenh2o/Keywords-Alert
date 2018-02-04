
from email.mime.text import MIMEText
import smtplib



#email
class send_email():
    add1 = 'lithiumHack2018'#@gmail.com
    psw = 'hack6666'
    host ='smtp.gmail.com'
    add2=str()
    text=str()
    msg=MIMEText('')
    server=smtplib.SMTP_SSL()
    def __init__(self, text, add_to):
        self.add2 =add_to
        self.text=text
        self.msg =MIMEText(text,'plain','utf-8')
        self.login
        self.send()
        self.server.quit()

    def login():
        self.server = smtplib.SMTP_SSL(self.host, 465)
        self.server.login(add1,psw)

    def send():
        self.server.sendmail(add1, add2, msg.as_string())



#comparing
class compare_dict():
    a={}
    b={}
    b_minus_a ={}
    a_minus_b ={}



    def comparing(self,a,b):
        for key in b.keys():
            if not key in a.keys():
                self.b_minus_a[key] =b[key]
        for key in a.keys():
            if not key in b.keys():
                self.a_minus_b[key]=a[key]
    def __init__(self, a, b):
        self.a=a
        self.b=b
        self.comparing(a,b)


a ={'atc1':'aaa.com','atc2':'bbb.com'}
b=a.copy()
b['kkk']=8
a['ccc']=9
print(a)
print(b)

cmp = compare_dict(a,b)
kkk=cmp.a_minus_b.keys()
print(cmp.b_minus_a)
print(cmp.a_minus_b)
send_email(kkk,'weixuanlin.ca@outlook.com')
import os, time, datetime
import serial 
import smtplib 
import mimetypes 
import email 
import requests 

from ubidots import ApiClient 
from email.message import EmailMessage 
from email.parser import BytesParser, Parser 
from email.policy import default 

outbox_path = os.getcwd() + '/outbox/'

sender = "TYPE-SENDER-EMAIL-HERE" 
password = "SENDER-EMAIL-PASSWORD" 
recipient = "RECIPIENT-EMAIL-HERE" 

url = "http://www.google.com" 
timeout = 5 
connection = True

date = datetime.datetime.now() 

# Ubidots'tan Hareket Sensörlerinin değerlerini almaya yarayan fonksiyon 
def get_motion_values(): 
    api_mot = ApiClient(token='BBFF-lDanrqDe2yLDJA2LQ5xHFMGFQ1wZcF') 

    mot1 = api_mot.get_variable('5ffb87da1d8472552e4227b8').get_values(1)[0]['value'] 
    mot2 = api_mot.get_variable('60ad5c7b1d847265f56b40f1').get_values(1)[0]['value'] 
    
    return mot1, mot2 
    
# Ubidots'tan Su Sensörlerinin değerlerini almaya yarayan fonksiyon 
def get_water_values(): 
    api_wat = ApiClient(token='BBFF-pmlFh7Dl58flmIe5VdFWZEbpEoxLPS') 
    
    wat1 = api_wat.get_variable('5fe543fa4763e70c76ecf5c5').get_values(1)[0]['value'] 
    wat2 = api_wat.get_variable('60b3a9411d84726ec8055036').get_values(1)[0]['value'] 
    
    return wat1, wat2 
    
# Ekli/eksiz e-posta göndermeye yarayan fonksiyon 
def send_mail(subject, body, ek=None): 
    try:
        print('Trying to send Email...') 
        message = EmailMessage() 
        
        message['From'] = sender 
        message['To'] = recipient
        message['Subject'] = subject 
        message.set_content(body) 
        
        if ek: 
            dosya_adi = ek 
            ek = outbox_path + ek 
            mime_type, _ = mimetypes.guess_type(ek) 
            mime_type, mime_subtype = mime_type.split('/') 
            
            with open(ek, 'rb') as file: 
                message.add_attachment(file.read(), maintype=mime_type, subtype=mime_subtype, filename=dosya_adi) 
        
        mail_server = smtplib.SMTP_SSL('smtp.gmail.com') 
        mail_server.login(sender, password) 
        mail_server.send_message(message) 
        mail_server.quit() 
        print('Email sent succesfully.') 
        if ek: 
            os.remove(ek) 
    except: 
        print("Bir hata olustu!!") 
        with open(outbox_path + date.strftime("%Y%m%d_%H%M%S.eml"), 'w') as file: 
            gen = email.generator.Generator(file) 
            gen.flatten(message) 

# Gönderilemeyen e-postaları tekrar göndermeye yarayan fonksiyon 
def resend_mail(mails): 
    try: 
        for mail in mails: 
            with open(outbox_path + mail, 'rb') as file: 
                message = BytesParser(policy=default).parse(file) 
            print('Retrying to send Email...') 
            mail_server = smtplib.SMTP_SSL('smtp.gmail.com') 
            mail_server.login(sender, password) 
            mail_server.send_message(message) 
            mail_server.quit() 
            print('Email sent successfully.') 
            os.remove(outbox_path + mail) 
    except: 
        pass 
        
# SMS gönderme fonksiyonu 
def send_sms(sms): 
    port = serial.Serial("/dev/serial0", baudrate=115200, timeout=2) 
    sms_bytes = bytes(sms , 'utf-8') 
    
    try: 
        print('Trying to send SMS...') 
        port.write(b'AT+CPIN?\n') 
        time.sleep(1) 
        port.write(b'AT+CMGF=1\n') 
        time.sleep(1) 
        port.write(b'AT+CMGS="RECIPIENT-PHONE-NUMBER-HERE"\n')
        time.sleep(1) 
        port.write(sms_bytes) 
        time.sleep(1) 
        z = b'\x1a\n' 
        port.write(z) 
        rcv = port.readlines() 
        port.close 
        
        for msg in rcv: 
            if msg == b'ERROR\r\n': 
                raise Exception('SMS sending failed!!!') 
        print("SMS sent successfully.") 
        
    except: 
        print('SMS sending failed!!!') 
        with open(outbox_path + date.strftime("%Y%m%d_%H%M%S.sms"), 'w') as file: 
            file.write(sms) 
            
            
# Gönderilemeyen SMS'lerin tekrar gönderilmesini deneyen fonksiyon 
def resend_sms(smss): 
    for message in smss: 
    
        sending = True 
        
        with open(outbox_path + message, 'rb') as file: 
            sms_bytes = file.read() 
            
        port = serial.Serial("/dev/serial0", baudrate=115200, timeout=2) 
        
        port.write(b'AT+CPIN?\n') 
        time.sleep(1) 
        port.write(b'AT+CMGF=1\n') 
        time.sleep(1) 
        port.write(b'AT+CMGS="+905073374408"\n') 
        time.sleep(1) 
        port.write(sms_bytes) 
        time.sleep(1) 
        z = b'\x1a\n' 
        port.write(z) 
        rcv = port.readlines() 
        port.close 
        for msg in rcv: 
            if msg == b'ERROR\r\n': 
                sending = False 
        if sending: 
            os.remove(outbox_path + message) 
            
# İnternet kesintisinde SIM800L modülü ile E-posta gönderme fonksiyonu 
def send_email_with_sim800l(subject, body): 

    subject = bytes('AT+SMTPSUB="' + subject + '"\n', 'utf-8') 
    body_length = bytes('AT+SMTPBODY=' + len(body) + '\n', 'utf-8') 
    body = bytes(body, 'utf-8') 
    port = serial.Serial("/dev/serial0", baudrate=115200, timeout=2) 
    
    # GPRS Connection 
    port.write(b'AT+SAPBR=3,1,"APN","internet"\n')
    time.sleep(1) 
    port.write(b'AT+SAPBR=1,1\n') 
    time.sleep(1) 
    
    # Email Sending 
    port.write(b'AT+EMAILCID=1\n') 
    time.sleep(1) 
    port.write(b'AT+EMAILTO=60\n') 
    time.sleep(1) 
    port.write(b'AT+EMAILSSL=1\n') 
    time.sleep(1) 
    port.write(b'AT+SMTPSRV="smtp.gmail.com"\n') 
    time.sleep(1) 
    
port.write(b'AT+SMTPAUTH=1,"SENDER-EMAIL-HERE","SENDER-EMAIL-PASSWORD"\n') 
    time.sleep(1) 

port.write(b'AT+SMTPFROM="SENDER-EMAIL-HERE","SENDER-EMAIL-HERE"\n') 
    time.sleep(1) 
    port.write(subject) 
    time.sleep(1) 
    port.write(b'AT+SMTPRCPT=0,0,"RECIPIENT-EMAIL-HERE","RECIPENT-USERNAME"\n') 
    time.sleep(1) 
    port.write(body_length) 
    time.sleep(1) 
    port.write(body) 
    time.sleep(1) 
    port.write(b'AT+SMTPSEND\r\n') 
    time.sleep(15) 
    
    port.close() 
    
# Crontab sayesinde her 5 dakikada bir çağrılmak üzere ayarlanan, 
# 'outbox' klasöründeki dosyaları ve internet bağlantısını kontrol eden fonksiyon 
def check_outbox(): 
    try: 
        print('Checking connection...') 
        print('Wifi Connection is OK.\nChecking outbox...') 
        mails = [] 
        smss = [] 
        videos = [] 
        for file in os.listdir(outbox_path): 
            if file.endswith('.eml'): 
                mails.append(file) 
            if file.endswith('.sms'): 
                smss.append(file) 
            if file.endswith('.avi'): 
                videos.append(file) 
        if smss: 
            resend_sms(smss) 
        request = requests.get(url, timeout=timeout) 
        connection = True 
        
        if mails: 
            resend_mail(mails) 
            
        if videos:
            for video in videos: 
                send_mail('Ev Güvenlik Sistemi', 'Kamera aygıtı bir hareket algıladı ve bu hareket sonucu kaydedilen video ektedir.', video) 
                send_sms('Kamera aygıtı bir hareket algıladı ve kaydedilen video mail olarak gönderildi.\nVideo kaydedilme tarihi: {}'.format(str(date))) 
            else: 
                print('Outbox is empty') 
                
        except FileNotFoundError: 
            os.mkdir(outbox_path) 
        
        except (requests.ConnectionError, requests.Timeout) as exception: 
            if connection: 
                subject = 'Ev Güvenlik Sistemi' 
                body = 'Ev Guvenlik Sisteminin internet baglantisi kesildi.\nOlay Tarihi: ' + str(date) 
                send_email_with_sim800l(subject, body) 
                send_sms(body) 
                connection = False
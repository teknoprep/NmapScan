"""
NmapEmail.
**Author:** Chris Rawlings
**Created:** 08.26.2020
**whatever directory you install to please set in os.chdir('')
"""

import sys
import ssl
import smtplib
import subprocess
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase 
from email import encoders
from os.path import basename
from xml.dom import minidom
from datetime import datetime

sender_email = ""
sender_user = ""
password = ""
receiver_email = ""
default_address = ""
smtp_server = ""
smtp_port = ""
Customer_Name = ""
Customer_Subject = ""
#os.chdir('/usr/src/')

def main():
    """Start of the program."""
    # Types of errors to handel in the sys.argv if arg is missing.
    errors = (ValueError, IndexError)
    ip_a = ''
    try:
        arg = sys.argv[1]
        ip_a = sys.argv[2]
    except errors:
        print('Use -new and ip address to make a new template or -ip and ip address to do nmap scan\n')
        exit()
    nmap(arg, ip_a)


def nmap(arg, ip_a):
    """Run the nmap scan."""
    # Set the date and commands to copy nmap.xml and make new nmap.xml
    now = datetime.now()
    old_xml_time = now.strftime("%d.%m.%Y")
    xml_file_name = ip_a + '_nmap.xml'
    old_xml = 'cp', xml_file_name, xml_file_name + '_' + old_xml_time
    nmap_scan = 'nmap', ip_a, '-p', '-', '-oX', xml_file_name
    new_nmap_scan = 'nmap', ip_a, '-p', '-', '-oX', 'new_' + xml_file_name
    if arg == '-new':
        subprocess.call(old_xml)
        subprocess.call(nmap_scan)
    elif arg == '-ip':
        subprocess.call(new_nmap_scan)
        #new_ports(xml_file_name, ip_a)
    else:
        print('Use -new to make new template \
or just "python3 nmap_email.py" to run the program.')
    create_html(xml_file_name, ip_a)

def create_html(xml_file_name, ip_a):
    pattern = "\d+"
    path ="./"
    files = os.listdir(path)
    xml_file_name_new = "1.xml"
    xml_file_name_new_html = "1.html"
    
    try:
        os.remove(xml_file_name_new)
    except:
        print("File not there")
    
    try:
        os.remove(xml_file_name_new_html)
    except:
        print("that file should really be there")
        
    os.rename(xml_file_name,xml_file_name_new)    
    for file in files:
        pattern = re.compile(pattern)
        x=re.findall(pattern,file)
        if x :
            xml=file
            html=x[0]+".html"
        else:
            html = ""
        subprocess.call(['xsltproc',xml_file_name_new,'-o',html])
    print("------------------------------SUCESSSSS----------------------------------------------------")
    send_mail_new(send_from= sender_email, subject= Customer_Name, text="This is left blank for now", send_to= receiver_email, files= xml_file_name_new_html)

def send_mail_new(send_from: str, subject: str, text: str, send_to: list, files: str):

    send_to = default_address if not send_to else send_to
    body = text
    attachment = open(files, "rb")
    
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % files)
    msg.attach(p)
    email_text = msg.as_string() 
    
    smtp = smtplib.SMTP(host= smtp_server, port= smtp_port)
    smtp.login(sender_user,password)
    smtp.sendmail(send_from, send_to, email_text)
    smtp.close()

main()




import paramiko
import datetime
import os


def sendtopi(localfile):
    date = datetime.datetime.now()
    date_strf = date.strftime("%Y%m%d-%H%M%S")
    paramiko.util.log_to_file("paramiko.log")

    # Open a transport
    host,port = "192.168.1.99",22
    transport = paramiko.Transport((host,port))

    # Auth    
    username,password = "pi","raspberry"
    transport.connect(None,username,password)

    outbox_path=os.getcwd()+"/"

    # Go!    
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Download
    # filepath = "/home/pi/Desktop/functions.py"
    # localpath = "D:/"+date_strf+".py"
    # sftp.get(filepath,localpath)
    
    localpath = outbox_path+localfile
    filepath = "/home/pi/Desktop/outbox/"+localfile
    sftp.put(localpath,filepath)
    
    # Upload
    # filepath = localpath
    # localpath = "/home/pony.jpg"
    # sftp.put(localpath,filepath)

    # Close
    if sftp: sftp.close()
    if transport: transport.close()

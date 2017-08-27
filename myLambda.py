
import json
import urllib.parse
import boto3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


print ('Loading function')
REGION = "us-east-2";
rds = boto3.client("rds", region_name=REGION);
ses = boto3.client("ses", region_name=REGION);
s3 = boto3.client("s3", region_name=REGION);


def lambda_handler(event, context):
    #msg = json.dumps(event);
    msgJson = json.loads(event['Records'][0]['Sns']['Message']); 
    eventMsg = msgJson;
    print (eventMsg);
    dbMap = eventMsg['Trigger']['Dimensions'][0];
    dbInstName = dbMap['value'];
	
    response = rds.describe_db_instances(DBInstanceIdentifier=dbInstName);
    dbins = response['DBInstances'];
    dbin = dbins[0];
    dbarn = dbin['DBInstanceArn'];
    
    res = rds.list_tags_for_resource(ResourceName=dbarn);
    emailIdList = [];
    tagList = res['TagList'];
    for tag in tagList:
        if tag['Key'] == 'DBOwner':
            emailIdList.append(tag['Value']);
            
        if tag['Key'] == 'DB_Email':
            emailIdList.append(tag['Value']);
        
        
    
    print (emailIdList);
    stremailIdList = ",".join(str(x) for x in emailIdList)
    print (stremailIdList);
    
    s3 = boto3.resource('s3');
    bucket = s3.Bucket('customemail');
    body = '';
    for obj in bucket.objects.all():
	    key = obj.key;
	    print (key);
	    if key == 'template.txt':
		    body = obj.get()['Body'].read().decode('utf-8');
    
    body1 = str(body);
    
    body1 = body1.replace("\n","<br>");
    body1 = body1.replace(" ", "&nbsp;");
    for key, value in eventMsg.items():
        key1 = '{{'+key+'}}';
        body1 = body1.replace(key1, str(value));
        
    triggerInfo = eventMsg['Trigger'];
    
    for key, value in triggerInfo.items():
        key1 = '{{Trigger.'+key+'}}';
        if key != '{{Trigger.Dimensions.0.value}}':
             body1 = body1.replace(key1, str(value));
            
    body1 = body1.replace('{{Trigger.Dimensions.0.value}}',dbInstName);

    
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    host = os.environ['SMTPHOST']
    port = os.environ['SMTPPORT']
    mail_from = os.environ.get('MAIL_FROM')
    mail_to = 'rakesh.raman@bp.com' 
    mail_to_Cc = 'nagaraju.balusa@bp.com'
    mail_to_Bcc = stremailIdList
    print ('mail_to_Bcc..   '+mail_to_Bcc)
    #mail_to = os.environ.get('MAIL_TO') # separate multiple recipient by comma. eg: "abc@gmail.com, xyz@gmail.com"

    reply_to = os.environ['reply_to']
    subject = event['Records'][0]['Sns']['Subject']
    print ('Printing..   '+subject)
    toaddrs = mail_to
    ccaddrs = mail_to_Cc
    bccaddrs = mail_to_Bcc
    success = send_email(host, port, username, password, subject, body1, toaddrs, ccaddrs, bccaddrs, mail_from, reply_to)
    response = { "isBase64Encoded": False }
    if success:
        response["statusCode"] = 200
        response["body"] = "message sent"
    else:
        response["statusCode"] = 400
        response["body"] = "message sending failed"
    print (response);
	        
			
			
def send_email(host, port, username, password, subject, body, mail_to, mail_cc,mail_bcc, mail_from = None, reply_to = None):
    if mail_from is None: mail_from = username
    if reply_to is None: reply_to = mail_to
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['Bcc'] = mail_bcc
    msg['Cc'] =  mail_cc 

    htmlBody = MIMEText(body, 'html')
    msg.attach(htmlBody);

    #message = """From: %s\nTo: %s\nReply-To: %s\nSubject: %s\n\n%s""" % (mail_from, mail_to, reply_to, subject, body)
    print (msg.as_string())
    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(mail_from, msg['To'].split(",")+ msg['Cc'].split(",")+ msg['Bcc'].split(","), msg.as_string())
        print ("Email Sent")
        server.close()
        return True
    except Exception as ex:
        print (ex)
        return False
    
    
	

#!/usr/bin/python3
import boto3
region = "us-east-2"
session = boto3.Session(profile_name='ohio')
aws_ec2= session.client('ec2', region_name=region)
ec2_response=aws_ec2.list_instances()
counter=1
f = open('ec2__roles_ohio.csv','w')
f.write("RoleName,Instance Name")
f.write("\n")
#print(ec2_response)
for instancedetails in ec2_response["Instances"]:
	f.write(Instancedetails["Role"].split('/')[1]+",")
	f.write(Instancedetails["InstanceName"])
	f.write("\n")

f.close()
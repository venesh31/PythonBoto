#!/usr/bin/python3
import boto3
region = "eu-west-1"
session = boto3.Session(profile_name='ireland')
aws_ec2= session.client('ec2', region_name=region)
ec2_response=aws_ec2.describe_instances()
counter=1
#f = open('ec2__roles_ohio.csv','w')
print("RoleName,Instance Name")
print("\n")
#print(ec2_response)
for instancedetails in ec2_response["Instances"]:
	print(Instancedetails["Role"].split('/')[1]+",")
	print(Instancedetails["InstanceName"])
	print("\n")

#f.close()
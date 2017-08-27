#!/usr/bin/python3
import boto3
region = "eu-west-1"
session = boto3.Session(profile_name='ireland')
ec2_client = session.client('ec2', region_name=region)
ec2_response=ec2_client.describe_instances()
#print(ec2_response)
counter=1
f = open('ec2_iam_roles_'+region+'new.csv','w')
f.write("EC2 Instance ID,RoleName")
f.write("\n")
#print(ec2_response)
while(1>0):
	if "Reservations" in ec2_response:
		for ec2details in ec2_response["Reservations"]:
			for ec2instance in  ec2details["Instances"]:
				f.write(ec2instance["InstanceId"]+",")
				if "IamInstanceProfile" in ec2instance:
				#f.write(ec2instance["IamInstanceProfile"][Arn].split('/')[1]+",")
					f.write(ec2instance["IamInstanceProfile"]["Arn"].split('/')[1])
				#f.write(ec2instance["InstanceId"])
				f.write("\n")
		if "NextToken" in ec2_response:
			ec2_response=ec2_client.describe_instances(
				Marker = ec2_response["NextToken"]
			)
		else:
			f.close()
			break
	elif "NextToken" in ec2_response:
		ec2_response=ec2_client.describe_instances(
			Marker = ec2_response["NextToken"]
		)
	else:
		f.close()
		break
f.close()
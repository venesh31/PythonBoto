#!/usr/bin/python3
import boto3
region = "eu-west-1"
session = boto3.Session(profile_name='ireland')
ec2_client = session.client('ec2', region_name=region)
ec2_response=ec2_client.describe_instances()
#print(ec2_response)
counter=1
#f = open('ec2_iam_roles_'+region+'.csv','w')
print("EC2 Instance ID,RoleName")
print("\n")
#print(ec2_response)
while(1>0):
	if "Reservations" in ec2_response:
		for ec2details in ec2_response["Reservations"]:
			for ec2instance in  ec2details["Instances"]:
				#print(ec2instance["InstanceId"]+",")
				print(ec2instance["InstanceId"]+",")
				print(ec2instance["IamInstanceProfile"]["Arn"].split('/')[1])
				print(ec2instance["IamInstanceProfile"]["Id"])
				if "IamInstanceProfile" in ec2instance:
					#print(ec2instance["IamInstanceProfile"][Arn].split('/')[1]+",")
					if ec2instance["IamInstanceProfile"]["Arn"].split('/')[1] =="access-admin" :
						print(ec2instance["InstanceId"]+",")
						#print(ec2instance["IamInstanceProfile"]["Arn"].split('/')[1])
						#print(ec2instance["IamInstanceProfile"]["Id"])
						response = ec2_client.describe_iam_instance_profile_associations(
							Filters=[
								{
									'Name': 'instance-id',
									'Values': [
										ec2instance["InstanceId"],
									]
								},
							],
							MaxResults=123
						)
						print(response["IamInstanceProfileAssociations"][0]["AssociationId"])
						response = ec2_client.disassociate_iam_instance_profile(
							AssociationId=response["IamInstanceProfileAssociations"][0]["AssociationId"]
						)
						response = ec2_client.associate_iam_instance_profile(
							IamInstanceProfile={
								'Arn': 'arn:aws:iam::354706231380:instance-profile/aws-elasticbeanstalk-ec2-role',
								'Name': 'aws-elasticbeanstalk-ec2-role'
							},
							InstanceId=ec2instance["InstanceId"]
						)
						counter = counter +1
				else:
					print("\n\n"+ec2instance["InstanceId"]+"\n\n")
					response = ec2_client.associate_iam_instance_profile(
							IamInstanceProfile={
								'Arn': 'arn:aws:iam::354706231380:instance-profile/aws-elasticbeanstalk-ec2-role',
								'Name': 'aws-elasticbeanstalk-ec2-role'
							},
							InstanceId=ec2instance["InstanceId"]
					)
					counter = counter +1
				#print(ec2instance["InstanceId"])
				print("\n")
		if "NextToken" in ec2_response:
			ec2_response=ec2_client.describe_instances(
				Marker = ec2_response["NextToken"]
			)
		else:
			#f.close()
			break
	elif "NextToken" in ec2_response:
		ec2_response=ec2_client.describe_instances(
			Marker = ec2_response["NextToken"]
		)
	else:
		##f.close()
		break
#f.close()
print(counter)
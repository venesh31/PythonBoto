#!/usr/bin/python3
import boto3
region = "us-east-2"
session = boto3.Session(profile_name='ohio')
rds_session = session.client('rds', region_name=region)
rds_details=rds_session.describe_db_instances()
#print(rds_details)
counter=1
f = open('rds_iam_roles_'+region+'.csv','w')
f.write("DBInstanceIdentifier,RoleName")
f.write("\n")
#print(rds_details)
while(1>0):
	if "DBInstances" in rds_details:
		for db_instance in rds_details["DBInstances"]:
			f.write(db_instance["DBInstanceIdentifier"]+",")
			print(db_instance["DBInstanceIdentifier"]+",")
			if "DomainMemberships" in db_instance:
				#print(db_instance["DomainMemberships"])
				try:
					f.write(db_instance["DomainMemberships"][0]["IAMRoleName"])
					print(db_instance["DomainMemberships"][0]["IAMRoleName"])
				except:
					print("")
				#if "Domain" in db_instance["DomainMemberships"]:
				#	print("TRUE")
				#	#f.write(db_instance["IamInstanceProfile"][Arn].split('/')[1]+",")
				#	#f.write(db_instance["DomainMemberships"]["IAMRoleName"].split('/')[1])
				#	print(db_instance["DomainMemberships"])
			#f.write(db_instance["InstanceId"])
			f.write("\n")
		if "Marker" in rds_details:
			rds_details=rds_session.describe_db_instances(
				Marker = rds_details["Marker"]
			)
		else:
			f.close()
			break
	elif "Marker" in rds_details:
		rds_details=rds_session.describe_db_instances(
			Marker = rds_details["Marker"]
		)
	else:
		f.close()
		break
f.close()
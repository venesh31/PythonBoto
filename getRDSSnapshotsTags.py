#!/usr/bin/python3
import boto3
region = "eu-west-1"
session = boto3.Session(profile_name='ireland')
rds_session = session.client('rds', region_name=region)
rds_details=rds_session.describe_db_instances()
#print(rds_details)
counter=1
f = open('rds_snashots_details_'+region+'.csv','w')
f.write("DBInstanceIdentifier,cloud-environment,repo-element-uid,DBOwner")
f.write("\n")
#print(rds_details)
while(1>0):
	if "DBInstances" in rds_details:
		for db_instance in rds_details["DBInstances"]:
			f.write(db_instance["DBInstanceIdentifier"]+",")
			print(db_instance["DBInstanceIdentifier"]+",")
			response = rds_session.list_tags_for_resource(
				ResourceName=db_instance["DBInstanceArn"]
			)
			#print(response)
			cloud_environment=True
			repo_element_uid=True
			DBOwner=True
			Tags={"cloud-environment":"","repo-element-uid":"","DBOwner":""}
			if "TagList" in response:
				#print(response["TagList"])
				for key in response["TagList"]:					
					if "Key" in key:
						if(key["Key"]=="cloud-environment"):
							#f.write(key["Key"])
							#f.write(key["Value"]+",")
							Tags[key["Key"]]=key["Value"]
						if(key["Key"]=="repo-element-uid"):
							#f.write(key["Key"]+",")
							#f.write(key["Value"]+",")
							Tags[key["Key"]]=key["Value"]
						if(key["Key"]=="DBOwner"):
							#f.write(key["Key"]+",")
							#f.write(key["Value"]+",")
							Tags[key["Key"]]=key["Value"]
			for key in Tags:
				f.write(Tags[key]+",")
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
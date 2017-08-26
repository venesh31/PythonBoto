#!/usr/bin/python3
import boto3
import time
region = "eu-west-1"
session = boto3.Session(profile_name='ireland')
rds_session = session.client('rds', region_name=region)
rds_details=rds_session.describe_db_snapshots()
#print(rds_details)
counter=1
f = open('deletesnapshots_'+region+'.csv','w')
f.write("DBSnapshotIdentifier,DBInstanceIdentifier,SnapshotType")
f.write("\n")
#print(rds_details)
while(1>0):
	if "DBSnapshots" in rds_details:
		for db_instance in rds_details["DBSnapshots"]:
			print(db_instance["DBSnapshotArn"])
			#print(db_instance["DBSnapshotIdentifier"]+",")
			print(db_instance["DBInstanceIdentifier"][0:3])
			#print(db_instance["SnapshotType"]+",")
			
			if(db_instance["DBInstanceIdentifier"][0:3]=="we1" or db_instance["DBInstanceIdentifier"][0:3]=="wu2"):
				# this block executes only when an instance have prefix like "we1" or "wu2"
				# This block deletes all snashots which are having above prefix
				print(db_instance["DBInstanceIdentifier"])
				print(db_instance["DBSnapshotIdentifier"])
				print(db_instance["DBSnapshotArn"])
				f.write(db_instance["DBSnapshotIdentifier"]+",")
				f.write(db_instance["DBInstanceIdentifier"]+",")
				f.write(db_instance["SnapshotType"]+",")
				delete_snapshot = rds_session.delete_db_snapshot(
					DBSnapshotIdentifier=db_instance["DBSnapshotIdentifier"]
				)			
				print(counter)
				counter=counter+1
				f.write("\n")
		if "Marker" in rds_details:
			rds_details=rds_session.describe_db_snapshots(
				Marker = rds_details["Marker"]
			)
		else:
			f.close()
			break
	elif "Marker" in rds_details:
		rds_details=rds_session.describe_db_snapshots(
			Marker = rds_details["Marker"]
		)
	else:
		f.close()
		break
f.close()
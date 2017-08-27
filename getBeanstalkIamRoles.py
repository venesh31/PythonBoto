#!/usr/bin/python3
import boto3
region = "eu-west-1"
session = boto3.Session(profile_name='ireland')
aws_elasticbeanstalk = session.client('elasticbeanstalk', region_name=region)
elasticbeanstalk=aws_elasticbeanstalk.describe_applications()
#print(elasticbeanstalk)
counter=1
f = open('beanstack_iam_roles_'+region+'.csv','w')
f.write("ApplicationName,RoleName")
f.write("\n")
#print(elasticbeanstalk)
while(1>0):
	if "Applications" in elasticbeanstalk:
		for bean in elasticbeanstalk["Applications"]:
			#f.write(bean["ApplicationName"]+",")
			print(bean["ApplicationName"]+",")
			if "ResourceLifecycleConfig" in bean:
				if "ServiceRole" in bean["ResourceLifecycleConfig"]:
					#f.write(bean["IamInstanceProfile"][Arn].split('/')[1]+",")
					f.write(bean["ResourceLifecycleConfig"]["ServiceRole"].split('/')[1])
					print(bean["ResourceLifecycleConfig"])
			#f.write(bean["InstanceId"])
			f.write("\n")
		if "NextToken" in elasticbeanstalk:
			elasticbeanstalk=aws_elasticbeanstalk.describe_applications(
				Marker = elasticbeanstalk["NextToken"]
			)
		else:
			f.close()
			break
	elif "NextToken" in elasticbeanstalk:
		elasticbeanstalk=aws_elasticbeanstalk.describe_applications(
			Marker = elasticbeanstalk["NextToken"]
		)
	else:
		f.close()
		break
f.close()
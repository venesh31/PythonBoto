#!/usr/bin/python3
import boto3
region = "us-east-2"
session = boto3.Session(profile_name='ohio')
#region = "eu-west-1"
#session = boto3.Session(profile_name='ireland')
lambda_session = session.client('lambda', region_name=region)
lambda_details=lambda_session.list_functions()
#print(lambda_details)
counter=1
f = open('test_lambda_copy_details_'+region+'.csv','w')
f.write("FunctionName,Subnets")
f.write("\n")
while(1>0):
	if "Functions" in lambda_details:
		for aws_lambda in lambda_details["Functions"]:
			f.write(aws_lambda["FunctionName"]+",")
			#print(aws_lambda["FunctionName"]+",")
			#print(aws_lambda["Runtime"]+"\t\t"+aws_lambda["Handler"]+"\t"+aws_lambda["Role"])
			if "VpcConfig" in aws_lambda:
				if "VpcId" in aws_lambda["VpcConfig"]:
					#print(aws_lambda["FunctionName"]+",\t\t"+aws_lambda["VpcConfig"]["VpcId"])
					#print(aws_lambda["VpcConfig"]["VpcId"])
					if len(aws_lambda["VpcConfig"]["VpcId"])>3:
						#print(str(counter)+"----"+aws_lambda["FunctionName"]+",\t\t"+aws_lambda["VpcConfig"]["VpcId"])
						for subnet in aws_lambda["VpcConfig"]["SubnetIds"]:
							#print(aws_lambda["VpcConfig"]["SubnetIds"])
							f.write(subnet+",")
							#print(subnet+",")
						#f.write("\n")
						counter = counter+1
			#print(aws_lambda)
			
			response = lambda_session.get_function(
				FunctionName=aws_lambda["FunctionName"],
				Qualifier=aws_lambda["Version"]
			)
			
			print(response)
			exit(1)
			f.write("\n")
		if "NextMarker" in lambda_details:
			lambda_details=lambda_session.list_functions(
				Marker = lambda_details["NextMarker"]
			)
		else:
			f.close()
			print("")
			break
	elif "NextMarker" in lambda_details:
		lambda_details=lambda_session.list_functions(
			Marker = lambda_details["NextMarker"]
		)
	else:
		f.close()
		print("")
		break
f.close()
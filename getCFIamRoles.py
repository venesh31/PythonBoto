#!/usr/bin/python3
import boto3
region = "us-east-2"
session = boto3.Session(profile_name='ohio')
aws_cloudformation = session.client('cloudformation', region_name=region)
cloudformation=aws_cloudformation.describe_stacks()
#print(cloudformation)
counter=1
f = open('cloudformation_iam_roles_'+region+'.csv','w')
f.write("StackName,RoleName")
f.write("\n")
#print(cloudformation)
while(1>0):
	if "Stacks" in cloudformation:
		for stack in cloudformation["Stacks"]:
			#f.write(stack["ApplicationName"]+",")
			f.write(stack["StackName"]+",")
			print(stack["StackName"]+",")
			#print(stack["ChangeSetId"]+",")
			#if "ChangeSetId" in stack:
			if "StackName" in stack:
				#print(stack["StackName"]+",")
				response = aws_cloudformation.get_template(
					StackName=stack["StackName"],
				)
				#print(type(response))
				#for key, value in response.items() :
				#	print (key)
				try:
					if "TemplateBody" in response:
						#print(response["TemplateBody"])
						objects=response["TemplateBody"]["Resources"]
						if "MyDB" in objects:
							if "Properties" in objects["MyDB"]:
								MonitoringRoleArn=objects["MyDB"]["Properties"]
								if "MonitoringRoleArn" in MonitoringRoleArn:
									Properties=MonitoringRoleArn["MonitoringRoleArn"]
									#print(type(Properties["Fn::Join"]))
									try:
										print("before Join")
										if "Fn::Join" in Properties:
											print("join starting")
											Roles=Properties["Fn::Join"]
											#print(Roles[1][2].split('/')[1])
											f.write(Roles[1][2].split('/')[1])
											print(Roles[1][2].split('/')[1])
									except TypeError:
										print("Type Error in Join")
				except:
					print("error")
				#print("TRUE")
			#if "Description" in stack:
			#	print(stack["Description"]+",")
			#	print("")
			if "RoleARN" in stack:
				#print(stack["RoleARN"])
				#print(stack["StackName"]+",")
				print("")
			f.write("\n")
			counter=counter+1
		if "NextToken" in cloudformation:
			cloudformation=aws_cloudformation.describe_stacks(
				NextToken = cloudformation["NextToken"]
			)
		else:
			f.close()
			break
	elif "NextToken" in cloudformation:
		cloudformation=aws_cloudformation.describe_stacks(
			NextToken = cloudformation["NextToken"]
		)
	else:
		f.close()
		break
f.close()
print(counter)
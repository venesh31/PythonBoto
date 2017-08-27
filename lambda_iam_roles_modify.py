#!/usr/bin/python3
import boto3
region = "eu-west-1"
session = boto3.Session(profile_name='ireland')
aws_lambda = session.client('lambda', region_name=region)
lambda_response=aws_lambda.list_functions()
counter=1
#f = open('lambda_roles_ohio.csv','w')
print("RoleName,Lambda Function Name")
print("\n")
#print(lambda_response)
while(1>0):
	if "Functions" in lambda_response:
		for lambdadetails in lambda_response["Functions"]:
			if lambdadetails["Role"].split('/')[1] =="lambda-vpc-execution-role" or "lambda_basic_execution" ==lambdadetails["Role"].split('/')[1]:
				print(lambdadetails["Role"].split('/')[1]+",")
				print(lambdadetails["FunctionName"])
				print("\n")
				if  "execute_data_query_lambda" != lambdadetails["FunctionName"] and "test-aws-rep" != lambdadetails["FunctionName"] and "test_7" != lambdadetails["FunctionName"] and lambdadetails["FunctionName"] != "test8":
					response=aws_lambda.update_function_configuration(
						FunctionName=lambdadetails["FunctionName"],
						Role="arn:aws:iam::354706231380:role/dbaas_Account-Services"
					)
				counter = counter + 1
		if "NextMarker" in lambda_response:
			lambda_response=aws_lambda.list_functions(
				Marker = lambda_response["NextMarker"]
			)
		else:
			#f.close()
			break
	elif "NextMarker" in lambda_response:
		lambda_response=aws_lambda.list_functions(
			Marker = lambda_response["NextMarker"]
		)
	else:
		#f.close()
		break
print(counter)
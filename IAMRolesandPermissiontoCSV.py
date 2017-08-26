#!/usr/bin/python3
import boto3
session = boto3.Session(profile_name='ireland')
iam = session.client('iam')
response = iam.list_roles(
    PathPrefix='/'
)
f = open('iam_roles_ireland.csv','w')
f.write("RoleName,Description,Policy Type, Policy Names")
f.write("\n")
while(1>0):
	if "Roles" in response:
		for role in response["Roles"]:
			if "RoleName" in role:
				f.write(role["RoleName"]+",")
			else:
				f.write(",")
			if "Description" in role:
				f.write(role["Description"]+",")	
			else:
				f.write(",")				
			responce_role_policies = iam.list_attached_role_policies(
				RoleName=role["RoleName"]
			)
			if "AttachedPolicies" in responce_role_policies:
				counter=1
				for policy in responce_role_policies["AttachedPolicies"]:
					if(counter>1):
						f.write("\n, ,Managed Policies,")
					else:
						f.write("Managed Policies,")	
					f.write(policy["PolicyName"])
					counter=counter+1
				f.write("\n, ,")	
			responce_role_inline_policies = iam.list_role_policies(
				RoleName=role["RoleName"]
			)
			if "PolicyNames" in responce_role_inline_policies:
				if "AttachedPolicies" not in responce_role_policies:
					f.write("\n, ,")
				counter=1
				for policy in responce_role_inline_policies["PolicyNames"]:
					if(counter>1):
							f.write("\n, ,Inline Policies,")
					else:
						f.write("Inline Policies,")
					f.write(policy)
					counter=counter+1
			
			f.write("\n")
	if "IsTruncated" in response:
		if response["IsTruncated"] == True:
			response = response = iam.list_roles(
				PathPrefix='/',
				Marker = response["Marker"]
			)
		else:
			f.close()
			break
	elif "IsTruncated" in response:
		if response["IsTruncated"] == True:
			response = response = iam.list_roles(
				PathPrefix='/',
				Marker = response["Marker"]
			)
	else:
		f.close()
		break
	
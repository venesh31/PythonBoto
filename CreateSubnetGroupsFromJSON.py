#!/usr/bin/python3
import boto3
import json
region = "us-east-2"
session = boto3.Session(profile_name='ohio')
rdsclient = boto3.client('rds', region_name=region)

deletionGroups = ["testsubnetgroup1", "testsubnetgroup2"]
json_data = open("testcreatesubnetgroup.json").read()

data = json.loads(json_data)
#print data
for i in data:
    ids = []
    print("Name:  " + i)
    print("Description:  " + data[i]["Properties"]["DBSubnetGroupDescription"])
    for x in data[i]["Properties"]["SubnetIds"]:
        ids.append(str(x))
    print("ids: ", ids)
    print(" ")
    print(" ")
    print(" ")
    rdsclient.create_db_subnet_group(
        DBSubnetGroupName="raju",
        DBSubnetGroupDescription="raju",
        SubnetIds=[
            'subnet-a7f229ce',
            'subnet-1b7c9560',
        ],
    )
    print("got here")



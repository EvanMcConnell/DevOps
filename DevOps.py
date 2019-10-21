#!/usr/bin/env python3
import boto3
import sys
import datetime
import urllib

ec2 = boto3.resource('ec2')

#Creation of instance
instance = ec2.create_instances(
	ImageId='ami-047bb4163c506cd98',
	MinCount=1,
	MaxCount=1,
	SecurityGroupIds=['sg-05b30b49b7d12d1eb'],
	InstanceType='t2.micro')

#Creation of Bucket
s3 = boto3.resource("s3")
try:
	#Create string using date and time, then format it to suit bucket requirements
	newBName = 'test-bucket-'+str(datetime.datetime.now())
	newBName = newBName.replace("-",".")
	newBName = newBName.replace(":",".")
	newBName = newBName.replace(" ","-")
	#Create bucket using string
	response = s3.create_bucket(Bucket=newBName, CreateBucketConfiguration={'LocationConstraint':'eu-west-1'})
	print (response)
except Exception as error:
	print (error)

#Downloading file from url
urllib.urlretrieve("http://devops.witdemo.net/image.jpg", "local-filename.jpg")
#Uploading file to bucket
s3.meta.client.upload_file("local-filename.jpg", newBName, 'image.jpg', ExtraArgs={'ACL':'public-read'})
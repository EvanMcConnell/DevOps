#!/usr/bin/env python3
print('/INTITIALIZING...')
import boto3
import sys
import datetime
import urllib
import os


ec2r = boto3.resource('ec2')
ec2c = boto3.client('ec2')
s3 = boto3.resource("s3")




print("""...
	/DONE
GENERATING INSTANCE NAME + USERDATA""")



#Create string using date and time, then format it to suit bucket requirements
newBName = 'test-bucket-'+str(datetime.datetime.now())
newBName = newBName.replace("-",".")
newBName = newBName.replace(":",".")
newBName = newBName.replace(" ","-")



print(newBName + """...
	/DONE
/CREATING BUCKET...""")



#Creation of Bucket
try:
	#Create bucket using string
	response = s3.create_bucket(Bucket=newBName, CreateBucketConfiguration={'LocationConstraint':'eu-west-1'})
	print (response)
except Exception as error:
	print (error)



print("""...
	/DONE
/DOWNLOADING FILE...""")



#Downloading file from url
urllib.urlretrieve("http://devops.witdemo.net/image.jpg", "local.jpg")

print("""...
	/DONE
/UPLOADING FILE TO BUCKET...""")



#Uploading file to bucket
s3.meta.client.upload_file("local.jpg", newBName, 'image.jpg', ExtraArgs={'ACL':'public-read'})

print("""...
	/DONE""")




#Assigning UserData code to be executed upon instance start
#user_data=	"""#!/bin/bash
#sudo yum update -y
#sudo yum -y install httpd
#systemctl enable httpd
#sudo service httpd start
#sudo su
#cd /var/www/html/
#echo '<html>' > index.html
#echo '<style type="text/css"> body{background-image: url("https://www.pixelstalk.net/wp-content/uploads/2016/05/Beautiful-cherry-blossom-wallpapers.jpg"); background-color: cyan;} p{color: white;} </style>' >> index.html
#echo '<body>' >> index.html
#echo '<p>Public IP Address: </p>'
#echo '<p>"""+public_ip_address+"""</p>' >> index.html
#echo '<p>Private IP address: </p>' >> index.html
#echo '<p>"""+private_ip_address+"""</p>' >> index.html
#curl http://"""+public_ip_address+"""/latest/meta-data/local-ipv4 >> index.html
#echo '<p>Here is the image:</p> ' >> index.html
#echo '<img src="https://s3-eu-west-1.amazonaws.com/""" + newBName + """/image.jpg">' >> index.html
#echo '</body> >> index.html"""


#print(user_data)
#keypair = ec2c.create_key_pair(KeyName=newBName)



print("""...
	/DONE
/CREATING EC2 INSTANCE...""")
#Creation of instance
print('/CREATING INSTANCE...')
instance = ec2r.create_instances(
	ImageId='ami-047bb4163c506cd98',
	MinCount=1,
	MaxCount=1,
	KeyName='key',
	SecurityGroupIds=['sg-05b30b49b7d12d1eb'],
	InstanceType='t2.micro',
	UserData = """#!/bin/bash
sudo yum update -y
sudo yum -y install httpd
systemctl enable httpd
sudo service httpd start
sudo su
cd /var/www/html/
echo '<html>' > index.html
echo '<style type="text/css"> body{background-image: url("https://www.pixelstalk.net/wp-content/uploads/2016/05/Beautiful-cherry-blossom-wallpapers.jpg"); background-color: cyan;} p{color: white;} </style>' >> index.html
echo '<body>' >> index.html
echo '<p>Public IP Address: </p>'
echo '<p>"""+instance[0].public_ip_address+"""</p>' >> index.html
echo '<p>Private IP address: </p>' >> index.html
echo '<p>"""+instance[0].private_ip_address+"""</p>' >> index.html
curl http://"""+instance[0].public_ip_address+"""/latest/meta-data/local-ipv4 >> index.html
echo '<p>Here is the image:</p> ' >> index.html
echo '<img src="https://s3-eu-west-1.amazonaws.com/""" + newBName + """/image.jpg">' >> index.html
echo '</body> >> index.html""")

print("""...
	/DONE
...
/WAITING FOR INSTANCE TO BE 'RUNNING'""")

instance[0].wait_until_running()
instance[0].reload()
ip=instance[0].public_ip_address
print(ip)
privip=instance[0].private_ip_address
print(privip)
#avzone=instance[0].availability_zone
#print(avzone)



os.system('ssh -i key.pem ec2.user@'+str(ip))
os.system('sudo su')
os.system('cd /var/www/html/')
os.system("echo '<p>Private IP Address: </p>' >> index.html")
os.system("echo "+str(privip)+" >> index.html")
#os.system("echo '<html>' > index.html")
#os.system("""echo '<style type="text/css"> body{background-image: url("https://www.pixelstalk.net/wp-content/uploads/2016/05/Beautiful-cherry-blossom-wallpapers.jpg"); background-color: cyan;} p{color: white;} </style>' >> index.html""")
#os.system("echo '<body>' >> index.html")
#os.system("echo '<p>Private IP address: </p>' >> index.html")
#os.system("curl http://"+str(ip)+"/latest/meta-data/local-ipv4 >> index.html")
#os.system("echo '<p>Availability Zone:: </p>' >> index.html")
#os.system("curl http://"+str(ip)+"/latest/meta-data/placement/availability-zone")
#os.system("echo '<p>Here is the image:</p> ' >> index.html")
#os.system("""echo '<img src="https://s3-eu-west-1.amazonaws.com/""" + newBName + """/image.jpg">' >> index.html""")
#os.system("echo '</body> >> index.html")




print("""...
	/DONE
...
	/EXITING""")
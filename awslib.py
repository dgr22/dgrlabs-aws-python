'''
.SYNOPSIS
	Library for All aws environment information
.NOTES
    Author: Destian Rezza
    Created: September 7, 2016
    Modified: 
'''

import boto3
from datetime import datetime, timedelta 

class AwsLib:

# === Initial Parameter === #

	today = datetime.now() + timedelta(days=1)
	one_weeks = timedelta(days=7)  
	start_date = today - one_weeks

	def __init__(self,key):
		self.region = "ap-southeast-1" 
		self.session = boto3.Session(profile_name=key, region_name=self.region)
		self.ec2 = self.session.resource("ec2")
		self.s3 = self.session.resource("s3")
		self.cloudwatch = self.session.client("cloudwatch")

# === Get Method === #

	def get_ec2_state(self,state):
		return self.ec2.instances.filter(
   					Filters=[{'Name': 'instance-state-name', 'Values': [state]}])

	def get_ebs_status(self,status):
		return self.ec2.volumes.filter(
					Filters=[{'Name': 'status', 'Values': [status]}])

	def get_interface_status(self,status):
		return self.ec2.network_interfaces.filter(
					Filters=[{'Name': 'status', 'Values': [status]}])

	def get_subnet_filter(self,tag_value):  
		return self.ec2.subnets.filter(
						Filters=[{'Name': 'tag:Name', 'Values': ['*'+tag_value+'*']}])

	def get_ec2_servergrouptype(self,tag_value,state):
		return self.ec2.instances.filter(
						Filters=[{'Name': 'tag:ServerGroupType', 'Values': ['*'+tag_value+'*']},
								 {'Name': 'instance-state-name', 'Values': [state]}])


# === Check Method === #

	def is_candidate_ec2_unused(self,instance_id):
		metricscw = self.cloudwatch.get_metric_statistics(
			Namespace='AWS/EC2',
			MetricName='CPUUtilization',
			Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
			Period=86400,  # every day
			StartTime=self.start_date,
			EndTime=self.today,
			Statistics=['Average'])

		metrics = metricscw['Datapoints']
		minimum = 0.05
		if metrics:
			for metric in metrics:
				average = metric['Average']
				if average > minimum:
					return False

		return True

# === Print Method === #

	def print_ec2_state(self,state):
		instances = self.get_ec2_state(state)
		for instance in instances:
			if instance.tags:
				for tag in instance.tags:
					if tag['Key'] == "Name":
						instance_name = tag['Value']
			else:
				instance_name = ""

			print(instance.id + " | " + instance_name)


	def print_ebs_status(self,status):
		volumes = self.get_ebs_status(status)
		for volume in volumes:
			if volume.tags:
				for tag in volume.tags:
					if tag['Key'] == "Name":
						volume_name = tag['Value']
			else:
				volume_name = ""

			print(volume.id + " | " + volume_name)


	def print_interface_status(self,status):
		interfaces = self.get_interface_status(status)
		for interface in interfaces:
			print(interface.id)


	def print_subnet_filter(self,tag_value):
		vpcs = self.get_subnet_filter(tag_value)
		for vpc in vpcs:
			for tag in vpc.tags:
				if tag['Key'] == "Name":
					vpc_name = tag['Value']
			print(vpc.id + " " + vpc_name)
		print()


	def print_ec2_servergrouptype(self,tag_value,state):
		instances = self.get_ec2_servergrouptype(tag_value,state)
		for instance in instances:
			if instance.tags:
				for tag in instance.tags:
					if tag['Key'] == "Name":
						instance_name = tag['Value']
			else:
				instance_name = ""

			print(instance.id + " | " + instance_name)

	def print_ec2_unused(self):
		running_instance = self.get_ec2_state("running")  
		candidate_instance = [  
		    instance
		    for instance in running_instance
		    if self.is_candidate_ec2_unused(instance.id)
		]

		if candidate_instance:
			print("================")
			print("=== Idle EC2 ===")
			print("================")
			i=0
			for candidate in candidate_instance:
				i=i+1  
				print(str([i]) + " " + candidate.id  + " | "
                    + candidate.tags[0]['Value']
                    + " | " + candidate.private_ip_address)

	def force_interface_delete(self):
		interfaces = self.get_interface_status("available")
		for interface in interfaces:
			print(interface.id)
			response = interface.delete()

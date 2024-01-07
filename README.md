# Monitoring, Scaling and Automation

## Create a S3 bucket

```py
import boto3

def create_s3_bucket(bucket_name):
    s3_client = boto3.client('s3')

    try:
        response = s3_client.create_bucket(Bucket=bucket_name)
        print(f"S3 bucket '{bucket_name}' created successfully.")
        return response['Location']
    except Exception as e:
        print(f"Error creating S3 bucket: {e}")
        return None

bucket_name = 'harsha'
s3_bucket_location = create_s3_bucket(bucket_name)
```

## Step 2: Launch an EC2 Instance and Deploy the Web Application


```
import boto3
import time

def launch_ec2_instance(instance_name, ami_id, instance_type, key_pair_name, security_group_ids, user_data_script):
    ec2_client = boto3.client('ec2')
    
    # Launch EC2 instance
    response = ec2_client.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_pair_name,
        SecurityGroupIds=security_group_ids,
        MinCount=1,
        MaxCount=1,
        UserData=user_data_script
    )

    instance_id = response['Instances'][0]['InstanceId']
    print(f"EC2 instance '{instance_id}' launched successfully.")

    return instance_id

# Example Usage
ami_id = 'your-ami-id'
instance_type = 't2.micro'
key_pair_name = 'harsha123'
security_group_ids = ['sg-xxxxxxxx']
user_data_script = '''
#!/bin/bash
# Your user data script for configuring the web server goes here
'''
instance_name = 'asg1'

instance_id = launch_ec2_instance(instance_name, ami_id, instance_type, key_pair_name, security_group_ids, user_data_script)

# Wait for the instance to be running
ec2_client = boto3.client('ec2')
ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])

```

## Step 1: Deploy an Application Load Balancer (ALB)


```py
import boto3

def create_alb(alb_name, subnet_ids, security_group_ids):
    elbv2_client = boto3.client('elbv2')

    try:
        # Create ALB
        response = elbv2_client.create_load_balancer(
            Name=alb_name,
            Subnets=subnet_ids,
            SecurityGroups=security_group_ids,
            Scheme='internet-facing',  # Adjust based on your requirements
            Tags=[{'Key': 'Name', 'Value': alb_name}]
        )

        alb_arn = response['LoadBalancers'][0]['LoadBalancerArn']
        print(f"ALB '{alb_name}' created successfully with ARN: {alb_arn}")
        
        return alb_arn
    except Exception as e:
        print(f"Error creating ALB: {e}")
        return None

# Example Usage
alb_name = 'asg1'
subnet_ids = ['subnet-xxxxxxxx', 'subnet-yyyyyyyy']  # Replace with your subnet IDs
security_group_ids = ['sg-xxxxxxxx']  # Replace with your security group ID

alb_arn = create_alb(alb_name, subnet_ids, security_group_ids)

```


## Step 2: Register EC2 Instance(s) with the ALB



```py
import boto3

def register_instances_with_alb(alb_arn, instance_ids):
    elbv2_client = boto3.client('elbv2')

    try:
        # Register EC2 instances with ALB
        elbv2_client.register_targets(
            TargetGroupArn=alb_arn,  # Replace with your ALB ARN
            Targets=[{'Id': instance_id} for instance_id in instance_ids]
        )

        print(f"EC2 instances {instance_ids} registered with ALB successfully.")
    except Exception as e:
        print(f"Error registering instances with ALB: {e}")

# Example Usage
instance_ids = ['i-xxxxxxxx', 'i-yyyyyyyy']  # Replace with your EC2 instance IDs
register_instances_with_alb(alb_arn, instance_ids)

```

## step 3 :

 
```py
import boto3

def register_instances_with_alb(alb_arn, target_group_name, instance_ids):
    elbv2_client = boto3.client('elbv2')

    try:
        response = elbv2_client.create_target_group(
            Name=target_group_name,
            Protocol='HTTP',
            Port=80,
            VpcId='your-vpc-id'  # Replace with your VPC ID
        )

        target_group_arn = response['TargetGroups'][0]['TargetGroupArn']

        # Register instances with ALB target group
        elbv2_client.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=[{'Id': instance_id} for instance_id in instance_ids]
        )

        # Attach target group to ALB
        elbv2_client.create_listener(
            DefaultActions=[{'Type': 'fixed-response', 'StatusCode': '200'}],
            LoadBalancerArn=alb_arn,
            Port=80,
            Protocol='HTTP',
            DefaultActions=[{'Type': 'forward', 'TargetGroupArn': target_group_arn}]
        )

        print(f"EC2 instances {instance_ids} registered with ALB successfully.")
    except Exception as e:
        print(f"Error registering instances with ALB: {e}")
```

## 1. Create an Auto Scaling Group (ASG):


```py
import boto3

def create_auto_scaling_group(asg_name, launch_config_name, min_size, max_size, desired_capacity, vpc_zone_identifier):
    autoscaling_client = boto3.client('autoscaling')

    try:
        # Create launch configuration
        autoscaling_client.create_launch_configuration

```

## 1. Lambda Function for Health Checks and Management:

```py
import boto3

def lambda_handler(event, context):
    # Replace with your ALB ARN, target group name, and SNS topic ARN
    alb_arn = 'your-alb-arn'
    target_group_name = 'your-target-group-name'
    sns_topic_arn = 'your-sns-topic-arn'

    elbv2_client = boto3.client('elbv2')
    autoscaling_client = boto3.client('autoscaling')
    ec2_client = boto3.client('ec2')
    sns_client = boto3.client('sns')

    # Perform health check by querying the ALB
    health_check_response = elbv2_client.describe_target_health(
        TargetGroupArn=alb_arn,
    )

    unhealthy_targets = [target['Target']['Id'] for target in health_check_response['TargetHealthDescriptions']
                         if target['TargetHealth']['State'] != 'healthy']

    # Check if health check consistently fails for any targets
    if unhealthy_targets:
        print(f"Unhealthy targets: {unhealthy_targets}")

        # Capture a snapshot of the failing instance
        for instance_id in unhealthy_targets:
            snapshot_response = ec2_client.create_snapshot(
                VolumeId=get_volume_id_from_instance_id(instance_id),
                Description=f"Health check failed for instance {instance_id}"
            )
            snapshot_id = snapshot_response['SnapshotId']
            print(f"Snapshot created for instance {instance_id}: {snapshot_id}")

            # Terminate the failing instance
            ec2_client.terminate_instances(InstanceIds=[instance_id])
            print(f"Instance {instance_id} terminated.")

            # Send notification through SNS to administrators
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Subject="Web Application Health Check Failure",
                Message=f"The web application health check failed for instance {instance_id}. "
                        f"Snapshot ID: {snapshot_id}. Instance terminated.",
            )

# Helper function to get volume ID from EC2 instance ID
def get_volume_id_from_instance_id(instance_id):
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    volume_id = response['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId']
    return volume_id

```
## 2. Set Up CloudWatch Events to Trigger Lambda:


* Configure CloudWatch Events to schedule the Lambda function to run periodically.

* Open the AWS Management Console.
Navigate to CloudWatch > Events > Rules.
Click "Create rule."
Select "Event Source" as "Event Source Type" and "Schedule" as "Event Source Details."
Set the schedule expression (e.g., rate(5 minutes) for a check every 5 minutes).
Add the Lambda function as a target for the rule.

## create an asg

```py
import boto3

def create_auto_scaling_group(asg_name, launch_config_name, min_size, max_size, desired_capacity, vpc_zone_identifier):
    autoscaling_client = boto3.client('autoscaling')

    try:
        # Create launch configuration
        autoscaling_client.create_launch_configuration(
            LaunchConfigurationName=launch_config_name,
            ImageId='your-ami-id',  # Replace with your AMI ID
            InstanceType='t2.micro',  # Replace with your desired instance type
            KeyName='your-key-pair',  # Replace with your key pair name
            SecurityGroups=['sg-xxxxxxxx'],  # Replace with your security group IDs
            UserData='your-user-data-script',  # Replace with your user data script
        )

        # Create Auto Scaling Group
        autoscaling_client.create_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            LaunchConfigurationName=launch_config_name,
            MinSize=min_size,
            MaxSize=max_size,
            DesiredCapacity=desired_capacity,
            VPCZoneIdentifier=vpc_zone_identifier,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'YourASGTag',
                    'PropagateAtLaunch': True
                },
            ],
        )

        print(f"Auto Scaling Group '{asg_name}' created successfully.")
    except Exception as e:
        print(f"Error creating Auto Scaling Group: {e}")

# Example Usage
asg_name = 'your-asg-name'
launch_config_name = 'your-launch-config-name'
min_size = 1
max_size = 3
desired_capacity = 2
vpc_zone_identifier = 'subnet-xxxxxxxx'  # Replace with your subnet ID

create_auto_scaling_group(asg_name, launch_config_name, min_size, max_size, desired_capacity, vpc_zone_identifier)

```

## 1. Configure ALB to Send Access Logs to S3 Bucket:

```py
import boto3

def configure_alb_logging(alb_arn, s3_bucket_name):
    elbv2_client = boto3.client('elbv2')

    try:
        response = elbv2_client.modify_load_balancer_attributes(
            LoadBalancerArn=alb_arn,
            Attributes=[
                {
                    'Key': 'access_logs.s3.enabled',
                    'Value': 'true',
                },
                {
                    'Key': 'access_logs.s3.bucket',
                    'Value': s3_bucket_name,
                },
            ]
        )

        print(f"ALB logging configured successfully.")
    except Exception as e:
        print(f"Error configuring ALB logging: {e}")

# Example Usage
alb_arn = 'your-alb-arn'
s3_bucket_name = 'your-s3-bucket-name'

configure_alb_logging(alb_arn, s3_bucket_name)

```

## 2. Create a Lambda Function Triggered by S3 Bucket:

```py
import boto3

def create_lambda_function(lambda_function_name, s3_bucket_name, sns_topic_arn):
    lambda_client = boto3.client('lambda')

    try:
        response = lambda_client.create_function(
            FunctionName=lambda_function_name,
            Runtime='python3.8',
            Role='your-lambda-execution-role-arn',  # Replace with your Lambda execution role ARN
            Handler='lambda_function.handler',
            Code={
                'S3Bucket': 'your-lambda-code-bucket',  # Replace with your Lambda code bucket
                'S3Key': 'lambda_function.zip',  # Replace with your Lambda code ZIP file
            },
            Environment={
                'Variables': {
                    'S3_BUCKET': s3_bucket_name,
                    'SNS_TOPIC_ARN': sns_topic_arn,
                },
            },
            Timeout=30,
        )

        print(f"Lambda function '{lambda_function_name}' created successfully.")
    except Exception as e:
        print(f"Error creating Lambda function: {e}")

# Example Usage
lambda_function_name = 'your-lambda-function-name'
sns_topic_arn = 'your-sns-topic-arn'

create_lambda_function(lambda_function_name, s3_bucket_name, sns_topic_arn)

```

##  Set Up Different SNS Topics:

```py
import boto3

def create_sns_topic(topic_name):
    sns_client = boto3.client('sns')

    try:
        response = sns_client.create_topic(Name=topic_name)
        topic_arn = response['TopicArn']
        print(f"SNS topic '{topic_name}' created successfully with ARN: {topic_arn}")
        return topic_arn
    except Exception as e:
        print(f"Error creating SNS topic: {e}")
        return None

```

## 2. Integrate SNS with Lambda for SMS or Email Notifications:

```py
import boto3

def subscribe_lambda_to_sns_topic(lambda_function_arn, sns_topic_arn):
    sns_client = boto3.client('sns')

    try:
        response = sns_client.subscribe(
            TopicArn=sns_topic_arn,
            Protocol='lambda',
            Endpoint=lambda_function_arn,
        )

        subscription_arn = response['SubscriptionArn']
        print(f"Lambda function subscribed to SNS topic successfully. Subscription ARN: {subscription_arn}")
    except Exception as e:
        print(f"Error subscribing Lambda function to SNS topic: {e}")


```

--------------------------------THE-END------------------------------------









































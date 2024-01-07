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


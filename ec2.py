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
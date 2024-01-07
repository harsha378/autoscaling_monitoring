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


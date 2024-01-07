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


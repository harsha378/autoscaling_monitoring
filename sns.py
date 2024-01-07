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


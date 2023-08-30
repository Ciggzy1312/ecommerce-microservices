import os
from dotenv import load_dotenv
import boto3
import json
from serializers.product import product_serializer

load_dotenv()
region = os.environ["AWS_REGION"]
access_key = os.environ["AWS_ACCESS_KEY"]
secret_key = os.environ["AWS_SECRET_KEY"]

async def basePublisher(topicName: str, data):
    try:
        sns = boto3.client(
            'sns',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

        response = sns.create_topic(Name=topicName)
        msg = sns.publish(
            TopicArn=response['TopicArn'],
            Message=json.dumps(product_serializer(data)),
        )

        return f"Message published to {topicName}", None
    except Exception as e:
        return None, e
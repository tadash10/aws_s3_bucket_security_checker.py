import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def monitor_cloudtrail_logs():
    cloudtrail_client = boto3.client('cloudtrail')

    # Retrieve the latest CloudTrail events
    events = cloudtrail_client.lookup_events(
        LookupAttributes=[{'AttributeKey': 'EventName', 'AttributeValue': 'ConsoleLogin'}],
        MaxResults=1
    )['Events']

    for event in events:
        event_name = event['EventName']
        event_time = event['EventTime']
        username = event['Username']
        
        logger.info(f"Monitoring CloudTrail logs for event: {event_name} at {event_time} by {username}")

        # Implement anomaly detection logic
        # For example, alert or take automated actions if unusual patterns are detected
        # ...


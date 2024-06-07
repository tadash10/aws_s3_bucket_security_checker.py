import boto3
import logging
from botocore.exceptions import BotoCoreError, NoCredentialsError, PartialCredentialsError

# Configure logging
logger = logging.getLogger('cloudtrail_monitor')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def monitor_cloudtrail_logs():
    cloudtrail_client = boto3.client('cloudtrail')

    try:
        # Retrieve the latest CloudTrail events
        response = cloudtrail_client.lookup_events(
            LookupAttributes=[{'AttributeKey': 'EventName', 'AttributeValue': 'ConsoleLogin'}],
            MaxResults=5  # Adjust as necessary
        )
        events = response['Events']

        if not events:
            logger.info("No ConsoleLogin events found.")
            return

        for event in events:
            event_name = event.get('EventName', 'N/A')
            event_time = event.get('EventTime', 'N/A')
            username = event.get('Username', 'N/A')
            source_ip = event.get('SourceIPAddress', 'N/A')  # Example additional info
            
            logger.info(f"Event: {event_name} | Time: {event_time} | User: {username} | IP: {source_ip}")

            # Implement anomaly detection logic
            if source_ip == 'unusual_ip':  # Placeholder logic
                logger.warning(f"Unusual login detected: {event_name} at {event_time} by {username} from {source_ip}")
                # Add alerting or automated response here

    except (NoCredentialsError, PartialCredentialsError) as e:
        logger.error(f"Credentials error: {e}")
    except BotoCoreError as e:
        logger.error(f"An error occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

# Example usage
monitor_cloudtrail_logs()

import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def update_security_patches():
    ec2_client = boto3.client('ec2')

    instances = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            logger.info(f"Updating security patches for instance: {instance_id}")

            try:
                ssm_client = boto3.client('ssm')
                response = ssm_client.send_command(
                    InstanceIds=[instance_id],
                    DocumentName="AWS-RunPatchBaseline",
                    TimeoutSeconds=600,
                )
                command_id = response['Command']['CommandId']
                logger.info(f"Command {command_id} sent successfully.")
            except Exception as e:
                logger.error(f"Failed to update security patches for instance {instance_id}: {str(e)}")

import boto3
import logging
from botocore.exceptions import ClientError

AWS_ALL_USERS_URI = 'http://acs.amazonaws.com/groups/global/AllUsers'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_buckets():
    """List all S3 buckets."""
    s3 = boto3.client('s3')
    try:
        response = s3.list_buckets()
        return response.get('Buckets', [])
    except ClientError as e:
        logger.error(f"Failed to list buckets: {str(e)}")
        return []

def get_bucket_acl(bucket_name):
    """Get ACL for a specific S3 bucket."""
    s3 = boto3.client('s3')
    try:
        acl = s3.get_bucket_acl(Bucket=bucket_name)
        return acl
    except ClientError as e:
        logger.error(f"Failed to get ACL for bucket {bucket_name}: {str(e)}")
        return {}

def is_bucket_insecure(bucket_permissions):
    """Check if a bucket has insecure permissions."""
    for permission in bucket_permissions:
        grantee = permission.get('Grantee', {})
        if 'URI' in grantee and AWS_ALL_USERS_URI in grantee['URI']:
            return True
    return False

def disable_bucket_access(bucket_name):
    """Disable public access for a specific bucket."""
    s3 = boto3.client('s3')
    try:
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )
        s3.put_bucket_acl(
            Bucket=bucket_name,
            AccessControlPolicy={'Grants': []}
        )
        return True
    except ClientError as e:
        logger.error(f"Failed to disable public access for bucket {bucket_name}: {str(e)}")
        return False

def enable_bucket_access(bucket_name):
    """Enable secure access for a specific bucket."""
    s3 = boto3.client('s3')
    try:
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        return True
    except ClientError as e:
        logger.error(f"Failed to enable secure access for bucket {bucket_name}: {str(e)}")
        return False

def process_buckets(buckets, access_function, message):
    """Process a list of buckets using the specified access function."""
    if buckets:
        logger.info(message)
        for bucket in buckets:
            if access_function(bucket):
                logger.info(f"Access updated for bucket: {bucket}")
            else:
                logger.warning(f"Failed to update access for bucket: {bucket}")
    else:
        logger.info(f"No buckets found for {message.split(' ')[0]}")

def main():
    insecure_buckets = [bucket['Name'] for bucket in list_buckets() if is_bucket_insecure(get_bucket_acl(bucket['Name']).get('Grants', []))]
    secure_buckets = [bucket['Name'] for bucket in list_buckets() if not is_bucket_insecure(get_bucket_acl(bucket['Name']).get('Grants', []))]

    process_buckets(insecure_buckets, disable_bucket_access, "Insecure S3 Buckets:")
    process_buckets(secure_buckets, enable_bucket_access, "Secure S3 Buckets:")

if __name__ == "__main__":
    main()

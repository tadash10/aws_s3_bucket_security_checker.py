import boto3
import logging
from botocore.exceptions import ClientError

AWS_ALL_USERS_URI = 'http://acs.amazonaws.com/groups/global/AllUsers'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class S3BucketManager:
    def __init__(self):
        self.s3 = boto3.client('s3')

    def list_buckets(self):
        try:
            response = self.s3.list_buckets()
            return response.get('Buckets', [])
        except ClientError as e:
            logging.error(f"Failed to list buckets: {e}")
            return []

    def get_bucket_acl(self, bucket_name):
        try:
            acl = self.s3.get_bucket_acl(Bucket=bucket_name)
            return acl
        except ClientError as e:
            logging.error(f"Failed to get ACL for bucket {bucket_name}: {e}")
            return {}

    def is_bucket_insecure(self, bucket_permissions):
        for permission in bucket_permissions:
            grantee = permission.get('Grantee', {})
            if 'URI' in grantee and AWS_ALL_USERS_URI in grantee['URI']:
                return True
        return False

    def disable_bucket_access(self, bucket_name):
        try:
            self.s3.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
            # Set the ACL to empty
            self.s3.put_bucket_acl(Bucket=bucket_name, AccessControlPolicy={'Grants': [], 'Owner': self.s3.get_bucket_acl(Bucket=bucket_name)['Owner']})
            return True
        except ClientError as e:
            logging.error(f"Failed to disable public access for bucket {bucket_name}: {e}")
            return False

    def enable_bucket_access(self, bucket_name):
        try:
            self.s3.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': False,
                    'IgnorePublicAcls': False,
                    'BlockPublicPolicy': False,
                    'RestrictPublicBuckets': False
                }
            )
            return True
        except ClientError as e:
            logging.error(f"Failed to enable secure access for bucket {bucket_name}: {e}")
            return False

    def process_buckets(self, buckets, access_function, message):
        if buckets:
            logging.info(message)
            for bucket in buckets:
                if access_function(bucket):
                    logging.info(f"Access updated for bucket: {bucket}")
                else:
                    logging.warning(f"Failed to update access for bucket: {bucket}")
        else:
            logging.info(f"No buckets found for {message.split(' ')[0]}")

def main():
    bucket_manager = S3BucketManager()

    all_buckets = bucket_manager.list_buckets()
    insecure_buckets = [bucket['Name'] for bucket in all_buckets if
                        bucket_manager.is_bucket_insecure(bucket_manager.get_bucket_acl(bucket['Name']).get('Grants', []))]
    secure_buckets = [bucket['Name'] for bucket in all_buckets if
                      not bucket_manager.is_bucket_insecure(bucket_manager.get_bucket_acl(bucket['Name']).get('Grants', []))]

    bucket_manager.process_buckets(insecure_buckets, bucket_manager.disable_bucket_access, "Insecure S3 Buckets:")
    bucket_manager.process_buckets(secure_buckets, bucket_manager.enable_bucket_access, "Secure S3 Buckets:")

if __name__ == "__main__":
    main()

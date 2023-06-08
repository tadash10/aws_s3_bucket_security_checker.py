import boto3

def list_insecure_s3_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    insecure_buckets = []

    for bucket in response.get('Buckets', []):
        bucket_name = bucket['Name']
        acl = s3.get_bucket_acl(Bucket=bucket_name)
        bucket_permissions = acl.get('Grants', [])

        for permission in bucket_permissions:
            grantee = permission.get('Grantee', {})
            if 'URI' in grantee and 'http://acs.amazonaws.com/groups/global/AllUsers' in grantee['URI']:
                insecure_buckets.append(bucket_name)
                break

    return insecure_buckets

def disable_insecure_s3_bucket_access(bucket_name):
    s3 = boto3.client('s3')

    try:
        # Remove public access block
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )

        # Remove public access permissions
        s3.put_bucket_acl(
            Bucket=bucket_name,
            AccessControlPolicy={
                'Grants': []
            }
        )

        return True
    except Exception as e:
        print(f"Failed to disable public access for bucket: {bucket_name}")
        print(f"Error: {str(e)}")
        return False

def list_secure_s3_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    secure_buckets = []

    for bucket in response.get('Buckets', []):
        bucket_name = bucket['Name']
        acl = s3.get_bucket_acl(Bucket=bucket_name)
        bucket_permissions = acl.get('Grants', [])

        secure = True
        for permission in bucket_permissions:
            grantee = permission.get('Grantee', {})
            if 'URI' in grantee and 'http://acs.amazonaws.com/groups/global/AllUsers' in grantee['URI']:
                secure = False
                break

        if secure:
            secure_buckets.append(bucket_name)

    return secure_buckets

def enable_secure_s3_bucket_access(bucket_name):
    s3 = boto3.client('s3')

    try:
        # Apply public access block
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
    except Exception as e:
        print(f"Failed to enable secure access for bucket: {bucket_name}")
        print(f"Error: {str(e)}")
        return False

def delete_all_objects_in_bucket(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    try:
        bucket.objects.all().delete()
        return True
    except Exception as e:
        print(f"Failed to delete objects in bucket: {bucket_name}")
        print(f"Error: {str(e)}")
        return False

def list_ec2_instances():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()

    instances = []
    for reservation in response.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            instance_id = instance.get('InstanceId')
            instances.append(instance_id)

    return instances

def stop_ec2_instances(instance_ids):
    ec2 = boto3.client('ec2')

    try:
        ec2.stop_instances(InstanceIds=instance_ids)
        return True
    except Exception as e:
        print("Failed to stop EC2 instances.")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    insecure_buckets = list_insecure_s3_buckets()

    if len(insecure_buckets) > 0:
        print("Insecure S3 Buckets:")
        for bucket in insecure_buckets:
            print(bucket)

        # Disable public access for insecure buckets
        for bucket in insecure_buckets:
            if disable_insecure_s3_bucket_access(bucket):
                print(f"Public access disabled for bucket: {bucket}")
            else:
                print(f"Failed to disable public access for bucket: {bucket}")
    else:
        print("No insecure S3 buckets found.")

    secure_buckets = list_secure_s3_buckets()

    if len(secure_buckets) > 0:
        print("Secure S3 Buckets:")
        for bucket in secure_buckets:
            print(bucket)

        # Enable secure access for secure buckets
        for bucket in secure_buckets:
            if enable_secure_s3_bucket_access(bucket):
                print(f"Secure access enabled for bucket: {bucket}")
            else:
                print(f"Failed to enable secure access for bucket: {bucket}")
    else:
        print("No secure S3 buckets found.")

    # Example usage: Delete all objects in a specific bucket
    # delete_all_objects_in_bucket('example-bucket')

    # Example usage: List EC2 instances
    # instances = list_ec2_instances()
    # if instances:
    #     print("EC2 Instances:")
    #     for instance_id in instances:
    #         print(instance_id)

    # Example usage: Stop EC2 instances
    # instance_ids = ['instance-1', 'instance-2']
    # if stop_ec2_instances(instance_ids):
    #     print("EC2 instances stopped successfully.")

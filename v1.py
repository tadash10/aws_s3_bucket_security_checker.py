import boto3

def list_insecure_s3_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    
    insecure_buckets = []
    
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        acl = s3.get_bucket_acl(Bucket=bucket_name)
        bucket_permissions = acl['Grants']
        
        for permission in bucket_permissions:
            grantee = permission['Grantee']
            if 'URI' in grantee and 'http://acs.amazonaws.com/groups/global/AllUsers' in grantee['URI']:
                insecure_buckets.append(bucket_name)
                break
    
    return insecure_buckets

def disable_insecure_s3_bucket_access(bucket_name):
    s3 = boto3.client('s3')
    
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

if __name__ == "__main__":
    insecure_buckets = list_insecure_s3_buckets()
    
    if len(insecure_buckets) > 0:
        print("Insecure S3 Buckets:")
        for bucket in insecure_buckets:
            print(bucket)
        
        # Disable public access for insecure buckets
        for bucket in insecure_buckets:
            disable_insecure_s3_bucket_access(bucket)
            print(f"Public access disabled for bucket: {bucket}")
    else:
        print("No insecure S3 buckets found.")

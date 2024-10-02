# AWS Security Checker

This script interacts with your AWS account to perform security checks and actions on AWS resources. This script make shure that  sensitive information such as  KEYS dont be public. 
thank you for the support 

# Installation

1. Ensure you have Python 3 installed on your system.
2. Clone or download this repository.
3. Install the required Python dependencies:

```bash
pip install boto3

    list_insecure_s3_buckets(): This function lists all S3 buckets and identifies insecure buckets that have public access permissions for the "AllUsers" group. It checks the bucket ACL (Access Control List) for any permissions granted to the "AllUsers" group.

    disable_insecure_s3_bucket_access(bucket_name): This function disables public access for a specific S3 bucket by removing the public access block and revoking any public access permissions in the bucket's ACL.

In the main section of the script, it first calls list_insecure_s3_buckets() to identify any insecure S3 buckets. If any insecure buckets are found, it prints their names and proceeds to disable public access for each insecure bucket using disable_insecure_s3_bucket_access(). Finally, it prints a confirmation message for each bucket where public access was disabled.

Usage

    Configure your AWS credentials using one of the following methods:
        AWS CLI Configuration
        Environment Variables

    Run the script using the following command:

bash

python aws_security_checker.py

    Follow the on-screen menu prompts to perform the desired actions:
        List Insecure S3 Buckets: Lists all S3 buckets with insecure access permissions.
        Disable Insecure S3 Bucket Access: Disables public access for a specified S3 bucket.
        List Secure S3 Buckets: Lists all S3 buckets with secure access permissions.
        Enable Secure S3 Bucket Access: Enables secure access for a specified S3 bucket.
        Delete All Objects in a Bucket: Deletes all objects in a specified S3 bucket.
        List EC2 Instances: Lists all EC2 instances in the AWS account.
        Stop EC2 Instances: Stops the specified EC2 instances.

Disclaimer

DISCLAIMER: This script interacts with your AWS account and can make changes to your resources. Ensure that you have the necessary permissions and use it responsibly. The script is provided as-is without any warranty. Use at your own risk..

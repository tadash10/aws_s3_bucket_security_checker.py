# aws_s3_bucket_security_checker.py

    list_insecure_s3_buckets(): This function lists all S3 buckets and identifies insecure buckets that have public access permissions for the "AllUsers" group. It checks the bucket ACL (Access Control List) for any permissions granted to the "AllUsers" group.

    disable_insecure_s3_bucket_access(bucket_name): This function disables public access for a specific S3 bucket by removing the public access block and revoking any public access permissions in the bucket's ACL.

In the main section of the script, it first calls list_insecure_s3_buckets() to identify any insecure S3 buckets. If any insecure buckets are found, it prints their names and proceeds to disable public access for each insecure bucket using disable_insecure_s3_bucket_access(). Finally, it prints a confirmation message for each bucket where public access was disabled.

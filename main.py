from patching import update_security_patches
from security_groups import analyze_security_groups
from sensitive_data_detection import detect_sensitive_data
from anomaly_detection import monitor_cloudtrail_logs
from key_rotation import rotate_access_keys

def main():
    # Call the new security functions
    update_security_patches()

    analyze_security_groups()

    detect_sensitive_data()

    monitor_cloudtrail_logs()

    rotate_access_keys()

if __name__ == "__main__":
    main()

import boto3
import os
from datetime import datetime

# Define variables
name = "watson"
s3_bucket = "codify-me-backup"
sqlite_db_path = f"/home/ec2-user/{name}/db/{name}.sqlite"  # Path to your SQLite DB
backup_dir = "/tmp/"  # Local directory to store temporary backups

# Initialize S3 client
s3 = boto3.client("s3")


def backup_sqlite_to_s3():
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_filename = f"{name}_{timestamp}.sqlite"
    backup_filepath = os.path.join(backup_dir, backup_filename)

    try:
        # Step 1: Copy SQLite DB file to a temporary backup location
        with open(sqlite_db_path, "rb") as db_file:
            with open(backup_filepath, "wb") as backup_file:
                backup_file.write(db_file.read())

        print(f"Database backup created at {backup_filepath}")

        # Step 2: Upload the backup to S3
        s3.upload_file(backup_filepath, s3_bucket, f"backups/{backup_filename}")
        print(f"Backup uploaded to S3: s3://{s3_bucket}/backups/{backup_filename}")

        # Step 3: Clean up (delete the local backup file if no longer needed)
        os.remove(backup_filepath)
        print(f"Local backup file removed: {backup_filepath}")

    except Exception as e:
        print(f"Error during backup: {str(e)}")


# Run the backup
backup_sqlite_to_s3()

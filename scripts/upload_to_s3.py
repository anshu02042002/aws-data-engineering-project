import boto3
from pathlib import Path 


# ----------------------------------------
# Project Paths
# ----------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"


# ----------------------------------------
# AWS S3 Configuration
# ----------------------------------------

BUCKET_NAME = "anshu-data-engineering-project-2026"

s3 = boto3.client("s3")


# ----------------------------------------
# Upload File to Amazon S3
# ----------------------------------------

def upload_file(file_name, s3_folder):

    local_file = RAW_DATA_PATH / file_name

    s3_key = f"{s3_folder}/{file_name}"

    s3.upload_file(
        str(local_file),
        BUCKET_NAME,
        s3_key
    )

    print(f"✅ {file_name} uploaded successfully!")


# ----------------------------------------
# Main Function
# ----------------------------------------

def main():

    upload_file(
        "customers.csv",
        "bronze/customers"
    )

    upload_file(
        "products.csv",
        "bronze/products"
    )

    upload_file(
        "orders.csv",
        "bronze/orders"
    )


if __name__ == "__main__":
    main()    
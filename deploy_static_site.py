import boto3
import json
import random
import string

def generate_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def deploy_s3_static_site():
    s3 = boto3.client('s3', region_name='ap-south-1')
    uid = generate_id()
    bucket_name = f"my-static-web-bucket-{uid}"
    
    print(f"Starting S3 Static Web Hosting Automation...")
    print(f"[INFO] Creating Bucket: {bucket_name}")
    
    # 1. Create Bucket
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'}
        )
        print("[OK] Bucket Created.")
    except Exception as e:
        print(f"Error creating bucket: {e}")
        return

    # 2. Disable Block Public Access
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
        print("[OK] Public Access Block removed.")
    except Exception as e:
        print(f"Error disabling public access block: {e}")

    # 3. Add Bucket Policy for Public Read Access
    try:
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }
        s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
        print("[OK] Bucket Policy attached (Public Read).")
    except Exception as e:
        print(f"Error setting bucket policy: {e}")

    # 4. Enable Static Website Hosting
    try:
        s3.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration={
                'ErrorDocument': {'Key': 'error.html'},
                'IndexDocument': {'Suffix': 'index.html'}
            }
        )
        print("[OK] Static Website Hosting enabled.")
    except Exception as e:
        print(f"Error enabling website hosting: {e}")

    # 5. Upload Website Code
    print("[INFO] Uploading website files...")
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key='index.html',
            Body=open('index.html', 'rb'),
            ContentType='text/html'
        )
        print("[OK] index.html uploaded successfully.")
    except Exception as e:
        print(f"Error uploading file: {e}")

    # Generate Website URL (Format for ap-south-1)
    website_url = f"http://{bucket_name}.s3-website.ap-south-1.amazonaws.com"
    
    print("\n============================================================")
    print("Deployment Complete!")
    print(f"Bucket Name: {bucket_name}")
    print(f"\nVisit your Static Website: {website_url}")
    print("============================================================")

if __name__ == "__main__":
    deploy_s3_static_site()

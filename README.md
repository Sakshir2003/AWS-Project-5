# AWS-Project-5
Automate Static Web Hosting on Amazon S3
This project demonstrates how to host a fully functional, highly scalable static website without provisioning a single server or EC2 instance. The entire infrastructure is automated using the Python Boto3 SDK.

What this Script Automates
Creates a unique S3 Bucket: Automatically generates a globally unique name for your bucket.
Disables "Block Public Access": AWS blocks public access by default. The script removes this blockade programmatically.
Attaches a Bucket Policy: Injects a custom JSON IAM policy that explicitly grants s3:GetObject permission to the public, turning the bucket into a public web directory.
Enables Static Website Hosting: Configures the bucket to act as an HTTP web server, routing default traffic to index.html.
Uploads the Website: Reads the local index.html file and pushes it to S3 with the precise ContentType='text/html' header (so browsers render it instead of downloading it).
How to Run
python deploy_static_site.py
After executing, the terminal will output your static website's public URL!

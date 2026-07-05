# AWS S3 Setup Guide

## 1. Create S3 Bucket

```bash
aws s3 mb s3://your-csip-audio-bucket --region us-east-1
```

## 2. Create IAM Policy (minimum permissions)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::your-csip-audio-bucket",
        "arn:aws:s3:::your-csip-audio-bucket/*"
      ]
    }
  ]
}
```

## 3. Create IAM User

```bash
aws iam create-user --user-name csip-uploader
aws iam put-user-policy --user-name csip-uploader --policy-name csip-s3-access --policy-document file://policy.json
aws iam create-access-key --user-name csip-uploader
```

## 4. Configure Environment

```env
AWS_ENABLED=true
STORAGE_PROVIDER=s3
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-csip-audio-bucket
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

## 5. Optional Lambda Trigger

Deploy `infra/aws/lambda/s3_upload_handler.py` and configure S3 event notification for `s3:ObjectCreated:*` on prefix `audio/`.

```bash
cd infra/aws/lambda
zip function.zip s3_upload_handler.py
aws lambda create-function \
  --function-name csip-s3-upload-logger \
  --runtime python3.11 \
  --handler s3_upload_handler.handler \
  --role arn:aws:iam::ACCOUNT:role/lambda-s3-role \
  --zip-file fileb://function.zip
```

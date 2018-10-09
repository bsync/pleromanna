# S3 Storage stuff....
YOUR_S3_BUCKET = "www.pleromabiblechurch.org"

STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_BUCKET_NAME_STATIC = YOUR_S3_BUCKET

# These next two lines will serve the static files directly
# from the s3 bucket
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % YOUR_S3_BUCKET
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

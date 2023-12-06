import os

from dotenv import load_dotenv

load_dotenv()

# COS secret key
COS_SECRET_KEY = os.getenv('COS_SECRET_KEY')

# COS secret id
COS_SECRET_ID = os.getenv('COS_SECRET_ID')

# COS target bucket
COS_BUCKET = os.getenv('COS_BUCKET')

# COS region
COS_REGION = os.getenv('COS_REGION')

# COS endpoint
COS_ENDPOINT = f'https://{COS_BUCKET}.cos.{COS_REGION}.myqcloud.com'

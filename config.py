import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DYNAMO_TABLES = [
        { 
            "TableName":"users",
            "KeySchema":[{
                "AttributeName":"id",
                "KeyType":"HASH"
            }],
            "AttributeDefinitions":[{
                "AttributeName":"id",
                "AttributeType":"S"
            },{
                "AttributeName":"username",
                "AttributeType":"S"
            },{
                "AttributeName":"email",
                "AttributeType":"S"
            }],
            "ProvisionedThroughput":{
                "ReadCapacityUnits":1,
                "WriteCapacityUnits":1
            },
            "GlobalSecondaryIndexes":[{
                "IndexName":"user_email",
                "KeySchema":[{
                    "AttributeName":"email",
                    "KeyType":"HASH"
                }],
                "Projection":{
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughput":{
                    "ReadCapacityUnits":1,
                    "WriteCapacityUnits":1
                }
            },{
                "IndexName":"user_username",
                "KeySchema":[{
                    "AttributeName":"username",
                    "KeyType":"HASH"
                }],
                "Projection":{
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughput":{
                    "ReadCapacityUnits":1,
                    "WriteCapacityUnits":1
                }
            }]
        }
    ]
    AWS_REGION = os.environ.get('AWS_REGION')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = [os.environ.get('ADMINS')]
    
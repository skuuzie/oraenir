import boto3
from config import logger

class OraenirDDB:
    def __init__(self) -> None:
        try:
            self.ddb = boto3.resource('dynamodb')
            logger.info('DynamoDB initialized')
        except:
            raise RuntimeError('dynamodb initialization failed.')
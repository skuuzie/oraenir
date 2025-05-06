from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource

import time

from .util import *
from util.exception import OraenirException
from config import logger, env

class ShortyCore:

    CORE_TABLE_NAME = env['DYNAMODB_TABLE']

    def __init__(self, ddb: DynamoDBServiceResource) -> None:
        """Initialize the DynamoDB service"""

        self.ddb = ddb
        self.table = self.ddb.Table(ShortyCore.CORE_TABLE_NAME)
        logger.info(f'DynamoDB table {ShortyCore.CORE_TABLE_NAME} is ready')
    
    def shorten_link(self, url: str, custom_id: str = None):
        """
        Shorten and store the original URL given the custom URL id, or else random identifier will be used
        
        returns the shortened url id
        """

        logger.info(f'Shortening: {url}')

        if not is_valid_url(url):
            logger.warning(f'Failed due to disallowed/invalid URL {url}')
            raise OraenirException('Invalid URL.', status_code=400)
        
        if custom_id:
            shorty = custom_id

            if not is_valid_url_id(shorty):
                logger.warning(f'Failed due to invalid custom ID: {shorty}')
                raise OraenirException('Your custom ID length must be 4-50 characters and consist of alphanumeric, hyphens (-), and underscores (_).', status_code=400)
            
            if self.table.get_item(Key={'id': shorty}).__contains__('Item'):
                logger.warning(f'Failed due to used custom ID: {shorty}')
                raise OraenirException('ID has been used.', status_code=400)
        else:
            while True:
                shorty = get_random_string(8)
                
                if not self.table.get_item(Key={'id': shorty}).__contains__('Item'):
                    break

        item = {
            'id': shorty,
            't': url,
            'ctime': time.time_ns()
        }

        self.table.put_item(
            Item=item
        )

        logger.warning(f'Created: {url} on /{shorty}')

        return shorty
    
    def open_shortened_link(self, id: str):
        """Extract the given url id and returns the original URL"""

        logger.info(f'Opening short URL: {id}')

        if not is_valid_url_id(id):
            logger.info(f'URL ID is disallowed: {id}')
            raise OraenirException('Invalid URL.', status_code=400)
        
        if not self.table.get_item(Key={'id': id}).__contains__('Item'):
            logger.info(f'URL ID doesnt exist')
            raise OraenirException('Invalid URL.', status_code=400)
        
        item = self.table.get_item(
            Key={
                'id': id
            }
        )

        logger.info(f"Ok. original URL: {item['Item']['t']}")

        return item['Item']['t']
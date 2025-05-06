from json import loads
from util.logger import CloudWatchLogger

env = loads(open('env.json', 'rb').read())
logger = CloudWatchLogger(region_name=env['CLOUDWATCH_REGION'], log_group_name=env['CLOUDWATCH_GROUP'], stream_name=env['CLOUDWATCH_STREAM'])
logger.info('LOG START')
import boto3
import datetime
import logging
import threading
from typing import Optional, Dict, Any

class CloudWatchLogger:
    """Logging class that integrates to AWS CloudWatch"""

    _instances: Dict[str, 'CloudWatchLogger'] = {}
    _instance_lock = threading.Lock()
    
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    
    def __new__(cls, region_name: str, stream_name: str, log_group_name: Optional[str] = None):
        key = f"{region_name}_{stream_name}_{log_group_name or stream_name}"
        
        with cls._instance_lock:
            if key not in cls._instances:
                instance = super().__new__(cls)
                cls._instances[key] = instance
            return cls._instances[key]
    
    def __init__(self, region_name: str, stream_name: str, log_group_name: Optional[str] = None):
        if hasattr(self, 'initialized'):
            return
            
        self.region_name = region_name
        self.stream_name = stream_name
        self.log_group_name = log_group_name or stream_name
        self.client = None
        self.sequence_token = None
        self.initialized = True
        
        self._init_client()
        
    def _init_client(self):
        self.client = boto3.client('logs', region_name=self.region_name)
        
        self._create_log_group_and_stream()
    
    def _create_log_group_and_stream(self):
        try:
            self.client.create_log_group(logGroupName=self.log_group_name)
        except self.client.exceptions.ResourceAlreadyExistsException:
            pass
        
        try:
            self.client.create_log_stream(
                logGroupName=self.log_group_name,
                logStreamName=self.stream_name
            )
        except self.client.exceptions.ResourceAlreadyExistsException:
            response = self.client.describe_log_streams(
                logGroupName=self.log_group_name,
                logStreamNamePrefix=self.stream_name
            )
            
            for stream in response.get('logStreams', []):
                if stream['logStreamName'] == self.stream_name:
                    self.sequence_token = stream.get('uploadSequenceToken')
                    break
    
    def _log(self, level: int, message: str, extra: Optional[Dict[str, Any]] = None):
        if not self.client:
            self._init_client()

        timestamp = int(datetime.datetime.now().timestamp() * 1000)
        
        level_name = logging.getLevelName(level)
        log_message = f"[{level_name}] {message}"

        if extra:
            log_message += f" - Extra: {extra}"
        
        params = {
            'logGroupName': self.log_group_name,
            'logStreamName': self.stream_name,
            'logEvents': [
                {
                    'timestamp': timestamp,
                    'message': log_message
                }
            ]
        }
        
        if self.sequence_token:
            params['sequenceToken'] = self.sequence_token
        
        try:
            response = self.client.put_log_events(**params)
            self.sequence_token = response.get('nextSequenceToken')
        except self.client.exceptions.InvalidSequenceTokenException as e:
            self.sequence_token = str(e).split("sequenceToken is: ")[-1].strip("'")
            params['sequenceToken'] = self.sequence_token
            response = self.client.put_log_events(**params)
            self.sequence_token = response.get('nextSequenceToken')
    
    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        self._log(self.DEBUG, message, extra)
    
    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        self._log(self.INFO, message, extra)
    
    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        self._log(self.WARNING, message, extra)
    
    def error(self, message: str, extra: Optional[Dict[str, Any]] = None):
        self._log(self.ERROR, message, extra)
    
    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None):
        self._log(self.CRITICAL, message, extra)
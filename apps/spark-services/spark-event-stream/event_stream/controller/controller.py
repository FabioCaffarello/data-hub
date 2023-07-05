import logging
from dataclasses import dataclass
from typing import Dict, Any
import json
from event_stream.config.config import JobConfig
import importlib

@dataclass
class MessageParameters:
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    status: Dict[str, Any]


class MessageProcessor:
    @staticmethod
    async def process_message(job_config: JobConfig, message_body: str):
        # Parse the message body and validate the fields
        print(job_config)
        message_params = MessageProcessor.parse_message_body(message_body)
        MessageProcessor.validate_message_params(message_params)

        # Perform additional processing or trigger a job based on the message data
        # ...
        # Import the module based on job_config.id
        module_name = f"event_stream.jobs.{job_config.id}"
        try:
            job_module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            logging.error(f"Module '{module_name}' not found")
            return

        # Trigger the job
        job_module.trigger_job(message_params.data)

    @staticmethod
    def parse_message_body(message_body: str) -> MessageParameters:
        try:
            parsed_body = json.loads(message_body)
        except json.JSONDecodeError as e:
            print(f"Failed to parse message body: {e}")
            raise ValueError("Invalid message body")

        message_data = parsed_body.get("data", {})
        message_metadata = parsed_body.get("metadata", {})
        message_status = parsed_body.get("status", {})

        print("Message body parsed successfully")
        return MessageParameters(data=message_data, metadata=message_metadata, status=message_status)

    @staticmethod
    def validate_message_params(message_params: MessageParameters):
        if not message_params.data:
            print("Invalid message: Missing data")
            raise ValueError("Invalid message: Missing data")
        # Additional validation rules
        # ...

        print("Message parameters validated successfully")


async def process_message(job_config, message_body: str):
    # print(job_config)
    await MessageProcessor.process_message(job_config, message_body)

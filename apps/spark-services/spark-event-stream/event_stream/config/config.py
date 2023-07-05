import os
import json
from dataclasses import dataclass


@dataclass
class JobConfig:
    id: str
    name: str

class ConfigService:
    def __init__(self):
        self.configs = {}

    def add_config(self, job_config: JobConfig):
        self.configs[job_config.id] = job_config

    def get_config(self, config_id: str) -> JobConfig:
        return self.configs[config_id]

    def get_all_configs(self) -> list:
        return list(self.configs.values())


def load_configs_from_directory(directory: str) -> ConfigService:
    config_service = ConfigService()
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                config_data = json.load(file)
                job_config = JobConfig(**config_data)
                config_service.add_config(job_config)

    return config_service

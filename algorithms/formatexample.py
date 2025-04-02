from utils.LocalModelGenerator import LocalModelGenerator
import yaml
import logging

class Formatexample:
    def __init__(self,
                 config_path = "config.yaml",
                 ):
        self.config = self.load_config(config_path)

    def load_config(self,config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config

    def generate_example(self):
        generator = LocalModelGenerator(**self.config)
        return
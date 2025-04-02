from utils.LocalModelGenerator import LocalModelGenerator
from utils.Prompts import AnswerGeneratorPrompt
from utils.APIGenerator_aisuite import APIGenerator_aisuite
from utils.APIGenerator_request import APIGenerator_request
import yaml
import logging
import pandas as pd
from utils.Prompts import FormatPrompt

class Formatexample:
    def __init__(self,config: dict):
        self.config = config
        self.prompt = AnswerGeneratorPrompt()
        self.model_generator = self.__init_model__()
    
    def __init_model__(self):
        if self.config["generator_type"] == "local":
            return LocalModelGenerator(**self.config["local_model_generator"])
        elif self.config["generator_type"] == "aisuite":
            return APIGenerator_aisuite(**self.config["aisuite_model_generator"])
        elif self.config["generator_type"] == "request":
            return APIGenerator_request(**self.config["request_model_generator"])
        else:
            raise ValueError(f"Invalid generator type: {self.config['generator_type']}")
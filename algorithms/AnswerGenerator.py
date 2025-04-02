from utils.Prompts import AnswerGeneratorPrompt
from utils.LocalModelGenerator import LocalModelGenerator
from utils.APIGenerator_aisuite import APIGenerator_aisuite
from utils.APIGenerator_request import APIGenerator_request
import yaml
import logging
import pandas as pd

class AnswerGenerator:
    '''
    Answer Generator is a class that generates answers for given questions.
    '''
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
    
    def run(self):
        # read input file : accept jsonl file only
        dataframe = pd.read_json(self.input_file,lines=True)
        # check if input_prompt_key are in the dataframe
        if self.input_prompt_key not in dataframe.columns:
            key_list = dataframe.columns.tolist()
            raise ValueError(f"input_prompt_key: {self.input_prompt_key} not found in the dataframe, please check the input_prompt_key: {key_list}")
        # check if output_text_key are in the dataframe
        if self.output_text_key in dataframe.columns:
            key_list = dataframe.columns.tolist()
            raise ValueError(f"Found {self.output_text_key} in the dataframe, which leads to overwriting the existing column, please check the output_text_key: {key_list}")
        # generate text
        user_prompts = dataframe[self.input_prompt_key].tolist()
        answers = self.model_generator.generate_text(user_prompts)
        dataframe[self.output_text_key] = answers
        dataframe.to_json(self.output_file,orient="records",lines=True)


import random
import os
import pandas as pd
from utils import LocalModelGenerator, APIGenerator_aisuite, APIGenerator_request
from utils.Prompts import QuestionSynthesisPrompt

class QuestionGenerator():
    def __init__(self, config):
        self.config = config
        self.prompts = QuestionSynthesisPrompt()
    
    def __init_model__(self):
        if self.config["generator_type"] == "local":
            return LocalModelGenerator(self.config)
        elif self.config["generator_type"] == "aisuite":
            return APIGenerator_aisuite(self.config)
        elif self.config["generator_type"] == "request":
            return APIGenerator_request(self.config)
        else:
            raise ValueError(f"Invalid generator type: {self.config.generator_type}")
        
    def _reformat_prompt(self, dataframe):

        # check if input_prompt_key are in the dataframe
        if self.config.input_key not in dataframe.columns:
            key_list = dataframe.columns.tolist()
            input_key  = self.config.input_key
            raise ValueError(f"input_prompt_key: {input_key} not found in the dataframe, please check the input_prompt_key: {key_list}")
        
        # predefined transformations options
        diversity_mode = [
            "1, 2, 3",
            "1, 2, 4",
            "1, 2, 5",
            "1, 4, 5",
            "1, 2, 3, 4, 5"
        ]

        formatted_prompts = []
        for question in dataframe[self.config.input_key]:
            selected_items = random.choice(diversity_mode)  # transformation combination for each question
            used_prompt = self.prompts.question_synthesis_prompt(selected_items, question)
            formatted_prompts.append(used_prompt.strip())

        return formatted_prompts
    
    def run(self):
        # read input file : accept jsonl file only
        dataframe = pd.read_json(self.config.input_file,lines=True)
        model = self.__init_model__()
        formatted_prompts = self._reformat_prompt(dataframe)
        responses = model.generate_text_from_input(formatted_prompts)

        if self.config.output_key in dataframe.columns:
            key_list = dataframe.columns.tolist()
            raise ValueError(f"Found {self.output_text_key} in the dataframe, which leads to overwriting the existing column, please check the output_text_key: {key_list}")
        
        dataframe[self.config.output_key] = responses
        output_dir = os.path.dirname(self.config.output_file)
        os.makedirs(output_dir, exist_ok=True)

        # Save DataFrame to JSON
        dataframe.to_json(self.config.output_file, orient="records", lines=True, force_ascii=False)

        return

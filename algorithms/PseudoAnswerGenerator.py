from utils.Prompts import AnswerGeneratorPrompt
from utils.LocalModelGenerator import LocalModelGenerator
from utils.APIGenerator_aisuite import APIGenerator_aisuite
from utils.APIGenerator_request import APIGenerator_request
from collections import defaultdict, Counter
from .AnswerExtraction_qwenmatheval import AnswerExtraction_qwenmatheval
import yaml
import logging
import pandas as pd

class PseudoAnswerGenerator:
    '''
    Pseudo Answer Generator is a class that generates answers for given questions, then choose the most frequent answer.
    '''
    def __init__(self,config: dict):
        self.config = config
        self.prompt = AnswerGeneratorPrompt()
        self.input_file = self.config["input_file"]
        self.output_file = self.config["output_file"]
        self.input_key = self.config["input_key"]
        self.output_key = self.config["output_key"]
        self.max_times = self.config["max_times"]
        self.model_generator = self.__init_model__()
        self.extractor = AnswerExtraction_qwenmatheval(self.config) 
    
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
        if self.input_key not in dataframe.columns:
            key_list = dataframe.columns.tolist()
            raise ValueError(f"input_key: {self.input_prompt_key} not found in the dataframe, please check the input_key: {key_list}")
        # check if output_text_key are in the dataframe
        if self.output_key in dataframe.columns:
            key_list = dataframe.columns.tolist()
            raise ValueError(f"Found {self.output_key} in the dataframe, which leads to overwriting the existing column, please check the output_key: {key_list}")
        # generate text
        user_prompts = dataframe[self.input_key].tolist()
        answer_dict = defaultdict(list)
        solution_dict = defaultdict(list)
        for i in range(self.max_times):
            solutions = self.model_generator.generate_text_from_input(user_prompts)
            answers = [self.extractor.answer_extractor.extract_answer(solution, self.extractor.data_name) for solution in solutions]
            for idx, answer in enumerate(answers):
                answer_dict[idx].append(answer)
                solution_dict[idx].append((answer, solutions[idx]))
        dataframe['extracted_answers'] = dataframe.get('extracted_answers', None) 
        dataframe['correct_solutions'] = dataframe.get('correct_solutions', None) 
        for key, value in answer_dict.items():
            count = Counter(value)
            final_answer = count.most_common(1)[0][0]
            dataframe.at[int(key),"extracted_answers"] = value
            dataframe.at[int(key),"final_answer"] = final_answer
            correct_contents = [content for ans, content in solution_dict[key] if ans == final_answer]
            dataframe.at[int(key), "correct_solutions"] = correct_contents
        dataframe.to_json(self.output_file,orient="records",lines=True)


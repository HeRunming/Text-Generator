import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from xVerify_custom.src.xVerify.model import Model
from xVerify_custom.src.xVerify.custommodel import Model_custom
from xVerify_custom.src.xVerify.eval import Evaluator


class AnswerJudger_xverify:
    '''
    An algorithm to judge if the two answers are the same based on xVerify
    '''
    def __init__(self,configs:dict):
        self.configs = configs
        self.check_config()

    def check_config(self):
        necessary_keys = ['input_file',
                          'output_file',

        ]
        for key in necessary_keys:
            if key not in self.configs:
                raise ValueError(f"The key {key} is not in the configs")

    def run(self):
        raw_dataframe = pd.read_json(self.configs['input_file'],lines=True)
        # check key for question
        if self.configs['question_key'] not in raw_dataframe.columns:
            raise ValueError(f"The key {self.configs['question_key']} is not in the dataframe")
        # check key for answer_1
        if self.configs['answer_1_key'] not in raw_dataframe.columns:
            raise ValueError(f"The key {self.configs['answer_1_key']} is not in the dataframe")
        # check key for answer_2
        if self.configs['answer_2_key'] not in raw_dataframe.columns:
            raise ValueError(f"The key {self.configs['answer_2_key']} is not in the dataframe")
        
        # check output key
        if self.configs['output_key'] in raw_dataframe.columns:
            raise ValueError(f"The key {self.configs['output_key']} is already in the dataframe, Please use another key")
        
        inference_mode = self.configs['inference_mode']
        if inference_mode not in ['api','local','custom']:
            raise ValueError(f"The inference_mode {inference_mode} is not supported, Please use 'api' or 'local' or 'custom'")
        
        if inference_mode == 'custom':
            model = Model_custom(model_name=self.configs['model_name'],
                                 model_path_or_url=self.configs['model_path_or_url'],
                                 inference_mode = "api",
                                 api_key = self.configs['api_key'])
        else:
            model = Model(model_name=self.configs['model_name'],
                          model_path_or_url=self.configs['model_path_or_url'],
                          inference_mode = inference_mode,
                          api_key = self.configs['api_key'])
        
        evaluator = Evaluator(model=model,process_num=self.configs['process_num'])

        if self.configs['inference_mode'] != 'custom':
            results = [
                evaluator.evaluate(question=row[self.configs['question_key']],
                                   answer_1=row[self.configs['answer_1_key']],
                                   answer_2=row[self.configs['answer_2_key']])
                for index,row in raw_dataframe.iterrows()
            ]
        else:
            results = []
            def process_row(row,index):
                result = evaluator.evaluate(question=row[self.configs['question_key']],
                                             answer_1=row[self.configs['answer_1_key']],
                                             answer_2=row[self.configs['answer_2_key']])
                results.append((result,index))
            
            with ThreadPoolExecutor(max_workers=self.configs['process_num']) as executor:
                executor.map(process_row,raw_dataframe.iterrows())
            
            results.sort(key=lambda x:x[1])
            results = [result[0] for result in results]

        raw_dataframe[self.configs['output_key']] = results
        raw_dataframe.to_json(self.configs['output_file'],orient='records',lines=True)

        return
        
                

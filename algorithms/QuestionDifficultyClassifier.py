import json
import os
import pandas as pd
from utils import LocalModelGenerator, APIGenerator_aisuite, APIGenerator_request
from utils.Prompts import QuestionCategoryPrompt

class QuestionCategoryClassifier():
    def __init__(self, config):
        self.config = config
        self.prompts = QuestionCategoryPrompt()
    
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

        formatted_prompts = []
        for text in dataframe[self.config.input_key]:
            used_prompt = self.prompts.question_synthesis_prompt(text)
            formatted_prompts.append(used_prompt.strip())

        return formatted_prompts
    
    def run(self):
        # read input file : accept jsonl file only
        dataframe = pd.read_json(self.config.input_file,lines=True)
        model = self.__init_model__()
        formatted_prompts = self._reformat_prompt(dataframe)
        responses = model.generate_text_from_input(formatted_prompts)

        for (idx, row), classification_str in zip(dataframe.iterrows(), responses):            
            try:
                classification = json.loads(classification_str) if classification_str else {}

                dataframe.at[idx, "primary_category"] = classification.get("primary_category", "")
                dataframe.at[idx, "secondary_category"] = classification.get("secondary_category", "")

            except json.JSONDecodeError:
                print(f"[警告] JSON 解析失败，收到的分类数据: {classification_str}")
            except Exception as e:
                print(f"[错误] 解析分类结果失败: {e}")

            except json.JSONDecodeError:
                print(f"JSON 解析失败，收到的分类数据: {classification_str}")
            except Exception as e:
                print(f"解析分类结果失败: {e}")


        if self.config.output_key in dataframe.columns:
            key_list = dataframe.columns.tolist()
            raise ValueError(f"Found {self.output_text_key} in the dataframe, which leads to overwriting the existing column, please check the output_text_key: {key_list}")
        
        output_dir = os.path.dirname(self.config.output_file)
        os.makedirs(output_dir, exist_ok=True)

        # Save DataFrame to JSON
        dataframe.to_json(self.config.output_file, orient="records", lines=True, force_ascii=False)
        
        return
import logging
import aisuite as ai
import pandas as pd
# APIKEY should be set in the environment variable


# 调用API生成文本
class APIGenerator_aisuite:
    def __init__(self, 
        model_id : str = 'openai:gpt-4o',
        temperature : float = 0.75,
        top_p : float = 1,
        max_tokens : int = 20,
        n : int = 1,
        stream : bool = False,
        stop = None,
        presence_penalty : float = 0,
        frequency_penalty : float = 0,
        logprobs = None,
        prompt : str = "You are a helpful assistant",
        input_file : str = None,
        output_file : str = None,
        input_prompt_key : str = "prompt",
        output_text_key : str = "response",
    ):
        logging.info(f"API Generator will generate text using {model_id}")
        self.model_id = model_id # must be <provider:modelname>
        # for model on huggingface, use <huggingface:modelname> 
        # (and don't forget provide your huggingface token in the environment variable or in the config file)
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.n = n
        self.stream = stream
        self.stop=stop
        self.presence_penalty=presence_penalty
        self.frequency_penalty=frequency_penalty
        self.prompt = prompt
        self.logprobs = logprobs


    
    def generate_batch(self):
        client = ai.Client()
        models = self.model_id.split(',')
        outputs = []
        
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
        for user_prompt in user_prompts:
            messages = [
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": user_prompt}
                ]
            response = client.chat.completions.create(
                    model=self.model_id,
                    messages=messages,
                    temperature=self.temperature,
                    top_p = self.top_p,
                    max_tokens = self.max_tokens,
                    n = self.n,
                    stream = self.stream,
                    stop = self.stop,
                    logprobs = self.logprobs,
                    presence_penalty = self.presence_penalty,
                    frequency_penalty = self.frequency_penalty,
            )
            content = response.choices[0].message.content
            # print(content)
            outputs.append(content)
        return outputs

    def generate_and_save(self):
        outputs = self.generate_batch()
        dataframe = pd.read_json(self.input_file,lines=True)
        dataframe[self.output_text_key] = outputs
        dataframe.to_json(self.output_file,orient='records',lines=True,force_ascii=False)

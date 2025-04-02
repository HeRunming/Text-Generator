import logging
from vllm import LLM,SamplingParams
from huggingface_hub import snapshot_download
import pandas as pd

class LocalModelGenerator:
    '''
    A class for generating text using vllm, with model from huggingface or local directory
    '''
    def __init__(
            self,
            device: str = "cuda",
            model_name_or_path: str = None,
            temperature: float = 0.7,
            top_p: float = 0.9,
            max_tokens: int = 100,
            top_k: int = 40,
            repetition_penalty: float = 1.0,
            seed: int = 42,
            prompt: str = "You are a helpful assistant",
            download_dir: str = "ckpr/models/",
            max_model_len: int = 4096,
            input_file: str = None,
            output_file: str = None,
            input_prompt_key: str = "prompt",
            output_text_key: str = "response",
    ):
        self.device = device
        self.real_model_path = snapshot_download(
            repo_id=model_name_or_path,
            local_dir=f"{download_dir}{model_name_or_path}",
        )
        logging.info(f"Model will be loaded from {self.real_model_path}")
        self.sampling_params = SamplingParams(
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            top_k=top_k,
            repetition_penalty=repetition_penalty,
            seed=seed,
        )
        self.llm = LLM(
            model=self.real_model_path,
            device=self.device,
            max_model_len=max_model_len,
        )
        self.prompt = prompt
        self.input_file = input_file
        self.output_file = output_file
        self.input_prompt_key = input_prompt_key
        self.output_text_key = output_text_key

    def generate_text(self):
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
        full_prompts = [self.prompt + '\n' + user_prompt for user_prompt in user_prompts]
        responses = self.llm.generate(full_prompts, self.sampling_params)
        return [output.outputs[0].text for output in responses]
    
    def generate_text_and_save(self):
        # generate text
        responses = self.generate_text()
        # save to output file
        dataframe = pd.read_json(self.input_file,lines=True)
        dataframe[self.output_text_key] = responses
        dataframe.to_json(self.output_file,orient="records",lines=True,force_ascii=False)
        return
    
    def generate_text_from_input(self,questions: list[str]) -> list[str]:
        full_prompts = [self.prompt + '\n' + question for question in questions]
        responses = self.llm.generate(full_prompts, self.sampling_params)
        return [output.outputs[0].text for output in responses]
import random
import os
import pandas as pd
from utils import LocalModelGenerator, APIGenerator_aisuite, APIGenerator_request
from utils.Prompts import QuestionSynthesisPrompt

class QuestionGenerator():
    def __init__(self, config):
        """
        Initialize the QuestionGenerator with the provided configuration.
        """
        self.config = config
        self.prompts = QuestionSynthesisPrompt()

        # Ensure the necessary configuration keys are provided
        self.input_file = self.config.get("input_file")
        self.output_file = self.config.get("output_file")
        self.input_key = self.config.get("input_key", "question")  # default key for question input
        self.output_key = self.config.get("output_key", "generated_question")  # default output key

        # Validate that input_file and output_file are provided
        if not self.input_file or not self.output_file:
            raise ValueError("Both input_file and output_file must be specified in the config.")

        # Initialize the model
        self.model = self.__init_model__()

    def __init_model__(self):
        """
        Initialize the model generator based on the configuration.
        """
        generator_type = self.config.get("generator_type", "local").lower()

        if generator_type == "local":
            return LocalModelGenerator(self.config)
        elif generator_type == "aisuite":
            return APIGenerator_aisuite(self.config)
        elif generator_type == "request":
            return APIGenerator_request(self.config)
        else:
            raise ValueError(f"Invalid generator type: {generator_type}")

    def _reformat_prompt(self, dataframe):
        """
        Reformat the prompts in the dataframe to generate questions.
        """
        # Check if input_key is in the dataframe
        if self.input_key not in dataframe.columns:
            key_list = dataframe.columns.tolist()
            raise ValueError(f"input_key: {self.input_key} not found in the dataframe. Available keys: {key_list}")

        # Predefined transformation options for diversity
        diversity_mode = [
            "1, 2, 3",
            "1, 2, 4",
            "1, 2, 5",
            "1, 4, 5",
            "1, 2, 3, 4, 5"
        ]

        formatted_prompts = []
        for question in dataframe[self.input_key]:
            selected_items = random.choice(diversity_mode)  # Randomly choose a transformation combination for each question
            used_prompt = self.prompts.question_synthesis_prompt(selected_items, question)
            formatted_prompts.append(used_prompt.strip())

        return formatted_prompts

    def run(self):
        """
        Run the question generation process.
        """
        try:
            
            # Read the input file (jsonl format only)
            dataframe = pd.read_json(self.input_file, lines=True)

            # Reformat the prompts for question generation
            formatted_prompts = self._reformat_prompt(dataframe)

            # Generate responses using the model
            responses = self.model.generate_text_from_input(formatted_prompts)

            # Ensure output_key doesn't already exist in the dataframe
            if self.output_key in dataframe.columns:
                raise ValueError(f"Found {self.output_key} in the dataframe, which would overwrite an existing column. Please use a different output_key.")

            # Store the generated responses in the dataframe
            dataframe[self.output_key] = responses

            # Ensure output directory exists
            output_dir = os.path.dirname(self.output_file)
            os.makedirs(output_dir, exist_ok=True)

            # Save DataFrame to JSON file
            dataframe.to_json(self.output_file, orient="records", lines=True, force_ascii=False)

            print(f"Generated questions saved to {self.output_file}")

        except Exception as e:
            print(f"[错误] 处理过程中发生异常: {e}")

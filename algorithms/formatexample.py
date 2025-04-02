import logging
import pandas as pd
from utils.Prompts import FormatPrompt

class Formatexample:
    def __init__(self,config):
        self.config = config
        self.prompts = FormatPrompt

    def _reformat_prompt(self):
        """
        reformat input jsonl's prompt for each algorithm, then save into input jsonl file
        """
        return
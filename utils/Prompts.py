'''
A collection of prompts for the text generator.
Every algorithm should contain its prompts in a class in this file.
'''

class FormatPrompt:
    '''
    No restrictions are required, the specific class to write depends on the specific algorithm.
    '''
    def __init__(self):
        pass

    def prompt_fuction_1(self,data: str) -> str:
        '''
        This is a function that takes a string as input and returns a string as output.
        '''
        return f"Please format the following text: {data}"
    
    def prompt_fuction_batch(self,data: list[str]) -> list[str]:
        '''
        This is a function that takes a list of strings as input and returns a list of strings as output.
        '''
        return [self.prompt_fuction_1(d) for d in data]
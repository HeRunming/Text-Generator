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


class AnswerGeneratorPrompt:
    '''
    The prompt for the answer generator.
    '''
    def __init__(self):
        pass

    def Classic_COT_Prompt(question: str) -> str:
        """
        为给定数学题目生成系统提示信息
        """
        prompt = (
            r'''You are an intelligent chatbot designed for writing the answer of the given math question.
    Remember: DO NOT output anything else, only output the answer you make.
    Generate a solution of a given math problem strictly following this format:
    1. Identify key components of the problem
    2. Apply theorems/formulas with step-by-step derivation
    3. Perform calculations with intermediate verification
    4. Final answer in \boxed{} notation

    Format Requirements:
    - Prefix each step with "→" (use the actual arrow symbol, not its Unicode escape sequence)
    - Ensure all symbols and special characters are presented using LaTeX commands where appropriate (e.g., ≥ as \\geq, ÷ as \\div)

    Example Template:
    Problem: Find the minimum value of function f(x) = x³ - 3x² + 4 on interval [-1, 3]

    Solution:
    1. Find critical points:
    → f'(x) = 3x² - 6x
    → Set derivative to zero: 3x(x-2) = 0 ⇒ x=0, x=2

    2. Evaluate function at critical points and endpoints:
    → f(-1) = (-1)^3 - 3(-1)^2 + 4 = -1 -3 +4 = 0.0000
    → f(0) = 0³ - 3(0)² +4 = 4.0000
    → f(2) = 8 - 12 +4 = 0.0000
    → f(3) = 27 - 27 +4 = 4.0000

    3. Compare values:
    → Minimum occurs at x=-1 and x=2

    Verification:
    → Second derivative test: f''(x) = 6x-6
    → f''(-1) = -12 < 0 (local max)
    → f''(2) = 6 > 0 (local min)

    \boxed{0}

    Here is the given problem you need to solve:
    '''
        )
        return prompt + question + r'''Your response must directly start with "Solution:" without any preamble, After the answer is generated finish your response right away.'''


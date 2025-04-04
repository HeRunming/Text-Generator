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
    

class QuestionSynthesisPrompt:
    '''
    The prompt for the question synthesis.
    '''
    def __init__(self):
        pass

    def question_synthesis_prompt(self,items, question):
        prompt = f"""
        Create a new reasonable and solvable math problem from the original problem by applying some of the following transformations(focus on all the transformations of "{items}"):

        1. Alter numerical values or expressions, ensuring the new problem remains solvable.
        2. Modify the problem type: introduce concepts like ratios or percentages, switch between derivatives and integrals, change the question from finding an area to finding a perimeter, etc.
        3. Contextualize the problem within a real-world scenario, such as incorporating various payment methods or deferred payments with interest.
        4. Add additional premises that require considering an extra factor separately in solving the problem.
        5. Increase the complexity of the problem by introducing multiple conditions that necessitate case-by-case analysis for a solution.

        Here is the problem from the user:
        {question}
        Write another problem inspired by this one.
        Not only change the problem scenario, but also try to create a new problem that requires another approach to solve.
        Start directly with the problem statement and DO NOT include any phrases such as "Here is a new problem inspired by a given one".
        After the problem is generated finish your response right away.
        """
        return prompt
    
class QuestionCategoryPrompt:
    '''
    The prompt for the question synthesis.
    '''
    def __init__(self):
        pass

    def question_synthesis_prompt(self, text):
        prompt = f"""
        You are a classification assistant specialized in mathematics. Your task is to classify the given text into one primary category and one secondary category according to the following taxonomy. Do not output any extra explanation. Return only a JSON object with the keys "primary_category" and "secondary_category".

        Taxonomy:
        1. Foundations and Logic
        - 1.1 Mathematical Logic and Set Theory
        - 1.2 Basic Theory, Formalization, and History & Education

        2. Algebra and Number Theory
        - 2.1 Linear Algebra and Group Theory
        - 2.2 Ring Theory, Field Theory, and Polynomial Algebra
        - 2.3 Commutative Algebra and Homological/Categorical Methods
        - 2.4 Number Theory
        - 2.5 Algebraic Geometry

        3. Analysis and Differential Equations
        - 3.1 Real Analysis, Measure Theory, and Functional Analysis
        - 3.2 Complex Analysis and Special Functions
        - 3.3 Differential Equations and Dynamical Systems
        - 3.4 Integral Transforms, Integral Equations, and Difference Equations
        - 3.5 Harmonic Analysis

        4. Geometry and Topology
        - 4.1 Euclidean, Analytic, and Convex/Discrete Geometry
        - 4.2 Differential Geometry and Manifold Theory
        - 4.3 Topology and Algebraic Topology

        5. Probability, Statistics, and Discrete Mathematics
        - 5.1 Probability Theory and Stochastic Processes
        - 5.2 Mathematical Statistics
        - 5.3 Combinatorics and Graph Theory

        6. Applied and Computational Mathematics
        - 6.1 Numerical Analysis and Computational Methods
        - 6.2 Optimal Control, Variational Methods, and Optimization
        - 6.3 Operations Research and Game Theory
        - 6.4 Systems Theory and Control
        - 6.5 Computer Science and Algorithms
        - 6.6 Mathematical Physics and Engineering Mathematics
        - 6.7 Information and Communication
        - 6.8 Biomathematics

        7. Arithmetic
        - 7.1 Basic Arithmetic and Number Operations
        - 7.2 Word Problems and Real-Life Applications

        Classify the following text into one primary category and one secondary category based on the taxonomy above. The text is:
        {text}
        """
        return prompt


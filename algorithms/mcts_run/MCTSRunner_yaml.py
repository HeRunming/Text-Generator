import os
import pathlib
import threading
from concurrent.futures import ThreadPoolExecutor
from MCTS.task import MCTS_Task
from utils.json_operator import load_file, dump_json
import copy
import time
import yaml
from openai import OpenAI


class MCTSRunner:
    def __init__(self, config=None):
        self.config = config
        self.file_lock = threading.Lock()
        self.output_list = []
        self.start_time = time.time()
        self.client = OpenAI(
            api_key=self.config['openai_api_key'],
            base_url=self.config['openai_api_base'],
        )
        
    def _process_task(self, i, data_list):
        data_list = pd.read_json(self.config['input_file'], lines=True)
        print(f'Begin to solve the problem {i + 1}...\n')
        data = data_list[i]['question']
        answer = data_list[i]['real_answer']

        Task = MCTS_Task(
            data, self.config['propose_method'], self.config['value_method'], self.config['branch'], self.config['end_gate'],
            self.config['roll_policy'], self.config['roll_branch'], self.config['roll_forward_steps'], self.config['time_limit'],
            self.config['iteration_limit'], self.config['exploration_constant'], self.config['alpha'], self.config['inf'],
            self.config['temperature'], use_case_prompt=self.config['use_case_prompt'], use_reflection=self.config['use_reflection'],
            low=self.config['low'], high=self.config['high'], evaluate=self.config['evaluate'], answer=answer, lang='en', client=self.client
        )

        output, root = Task.run()
        print(f'The solution to problem {i + 1} is complete.\n')

        base_dir = os.getcwd()
        output_dir = pathlib.Path(f'{base_dir}/outputs/{self.config["task_name"]}/{self.config["file"]}/{Task.mode}')
        output_file = self.config['output_file']
        data_item = copy.deepcopy(data_list[i])
        data_item['mcts_output'] = output

        with self.file_lock:
            pathlib.Path.mkdir(output_dir, exist_ok=True, parents=True)
            self.output_list.append(data_item)
            dump_json(output_file, self.output_list)

    def run(self):
        print('-' * 30, 'Begin testing', '-' * 30, '\n')
        file = self.config['load_file_path']
        print('** file_path: ', file)

        try:
            data_list = load_file(file)
            data_len = len(data_list)
        except Exception as e:
            print(f'File must be standardized json!\nError type:{e}\n')
            return

        assert data_len > 0, "Data list is empty!\n"

        with ThreadPoolExecutor(max_workers=32) as executor:
            futures = [executor.submit(self._process_task, i, data_list) for i in range(data_len)]
            for future in futures:
                future.result()

        print('_' * 60)
        print(f'Total number of questions: {data_len}\n')
        print('_' * 60)

        elapsed_time = time.time() - self.start_time
        print(f"程序运行时间: {elapsed_time:.2f} 秒")


def load_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


if __name__ == '__main__':
    config = load_config('config.yaml')
    runner = MCTSRunner(config=config)
    runner.run()
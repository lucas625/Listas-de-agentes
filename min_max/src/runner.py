from typing import List

from src.algorithm.min_max import MinMax
from src.helpers.input_reader import InputReader
from src.helpers.print_helper import PrintHelper


class Runner:

    def __init__(self, json_input_file_path: str):
        self.json_input_file_path = json_input_file_path

    def run(self):
        run_data = InputReader.read_data(self.json_input_file_path)
        min_max = MinMax(run_data)
        states = min_max.run()
        self._print_results(states)

    def _print_results(self, states: List[List[List[str]]]):
        print('----- Selected states -----')
        for (index, state) in enumerate(states):
            print(f'State {index}:\n{PrintHelper.state_to_str(state)}')

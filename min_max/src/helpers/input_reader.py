import json
from typing import List


class InputReader:

    @staticmethod
    def read_data(json_input_file_path: str) -> List[List[str]]:
        return InputReader._read_file(json_input_file_path).get('starting_state')

    @staticmethod
    def _read_file(json_input_file_path: str) -> dict:
        with open(json_input_file_path, 'r') as json_file:
            return json.load(json_file)

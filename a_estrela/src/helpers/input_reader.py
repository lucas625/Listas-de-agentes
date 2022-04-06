import json


class InputReader:

    @staticmethod
    def read_data(json_input_file_path: str) -> dict:
        json_data = InputReader._read_file(json_input_file_path)
        InputReader._add_reverse_connections()
        return json_data

    @staticmethod
    def _add_reverse_connections():
        pass

    @staticmethod
    def _read_file(json_input_file_path: str) -> dict:
        with open(json_input_file_path, 'r') as json_file:
            return json.load(json_file)

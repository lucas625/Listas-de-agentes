from src.helpers.input_reader import InputReader


class Runner:

    def __init__(self, json_input_file_path: str):
        self.json_input_file_path = json_input_file_path

    def run(self):
        run_data = InputReader.read_data(self.json_input_file_path)
        print(run_data)

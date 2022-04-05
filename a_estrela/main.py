from argparse import ArgumentParser
from argparse import Namespace

from src.runner import Runner


def _arguments_definition() -> Namespace:
    parser = ArgumentParser(description='Runs A*.')
    parser.add_argument(
        'json_input_file_path',
        type=str,
        help='Path to a json file.'
    )
    return parser.parse_args()


if __name__ == '__main__':
    arguments = _arguments_definition()
    runner = Runner(arguments)
    runner.run()

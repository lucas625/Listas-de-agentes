from typing import List


class PrintHelper:

    @staticmethod
    def state_to_str(state: List[List[str]]):
        return '\n'.join([str(line) for line in state])

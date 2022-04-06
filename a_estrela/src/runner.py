from src.algorithm.a_star import AStar
from src.data_structures.frontier_node import FrontierNode
from src.helpers.input_reader import InputReader


class Runner:

    def __init__(self, json_input_file_path: str):
        self.json_input_file_path = json_input_file_path

    def run(self):
        run_data = InputReader.read_data(self.json_input_file_path)
        start_node = run_data['start_node']
        target_node = run_data['target_node']
        speed = run_data['speed']
        a_star = AStar(
            run_data['nodes'],
            run_data['connections'],
            run_data['heuristics'],
            start_node,
            target_node
        )
        resulting_frontier_node = a_star.run()
        self._print_results(start_node, target_node, speed, resulting_frontier_node)

    def _print_results(self, start_node: str, target_node: str, speed: float, resulting_frontier_node: FrontierNode):
        if resulting_frontier_node:
            total_distance_string = '%.2f' % resulting_frontier_node.total_distance
            time_required_string = '%.2f' % (resulting_frontier_node.total_distance/speed)
            path_string = (
                f'{resulting_frontier_node.path} with {total_distance_string}km total distance. '
                f'Time required: {time_required_string}h'
            )
        else:
            path_string = 'Does not exist'
        print(f'Path from {start_node} to {target_node}: {path_string}')

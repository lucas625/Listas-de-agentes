import json
import math
from typing import List


class InputReader:

    @staticmethod
    def read_data(json_input_file_path: str) -> dict:
        json_data = InputReader._read_file(json_input_file_path)
        json_data['connections'] = InputReader._build_node_connections(json_data['connections'], json_data['nodes'])
        json_data['direct_distances'] = InputReader._build_node_connections(
            json_data['direct_distances'],
            json_data['nodes']
        )
        json_data['heuristics'] = InputReader._build_heuristics(
            json_data['direct_distances'],
            json_data['nodes'],
            json_data['target_node']
        )
        del json_data['direct_distances']
        return json_data

    @staticmethod
    def _build_node_connections(connections: list, nodes: List[str]) -> dict:
        dict_connections = {}
        for node in nodes:
            dict_connections[node] = []
        for connection in connections:
            dict_connections[connection['first_node']].append({
                'target': connection['second_node'],
                'distance': connection['distance']
            })
            dict_connections[connection['second_node']].append({
                'target': connection['first_node'],
                'distance': connection['distance']
            })
        return dict_connections

    @staticmethod
    def _build_heuristics(direct_distances: dict, nodes: List[str], target_node: str) -> dict:
        heuristic = {}
        for node in nodes:
            for connection in direct_distances[node]:
                if connection['target'] == target_node:
                    heuristic[node] = connection['distance']
        heuristic[target_node] = 0
        return heuristic

    @staticmethod
    def _read_file(json_input_file_path: str) -> dict:
        with open(json_input_file_path, 'r') as json_file:
            return json.load(json_file)

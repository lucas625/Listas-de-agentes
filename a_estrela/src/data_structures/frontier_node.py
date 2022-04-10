from typing import List


class FrontierNode:

    def __init__(self, name: str, total_distance: float, total_evaluation: float, path: List[str]):
        """
        :param name:
        :param total_distance: The sum of distances on the walked path.
        :param total_evaluation: The total distance + heuristic, the lesser, the greater the priority of the node.
        :param path: The nodes from start node to this node.
        """
        self.name = name
        self.total_distance = total_distance
        self.total_evaluation = total_evaluation
        self.path = path

    def __str__(self):
        return self.name

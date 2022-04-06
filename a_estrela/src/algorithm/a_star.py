from typing import List
from typing import Optional

from src.data_structures.frontier_node import FrontierNode


class AStar:
    """
    Members:
        nodes: list of node names.
        connections:
            dict where each key has list of connections.
            Each connection is like { target: node_name, distance: float }
        heuristics: dict where each key (node name) is a float estimating the distance to the target node.
        start_node: starting node name.
        target_node: target node name.
        frontier: list of ordered node names, based on their evaluation to get to the target node.
        dict_frontier: a dict where each key (node name) is a FrontierNode, used for optimizing the search.
        visited_nodes: list of node names that were already visited.
    """

    def __init__(self, nodes: List[str], connections: dict, heuristics: dict, start_node: str, target_node: str):
        self.nodes = nodes
        self.connections = connections
        self.heuristics = heuristics
        self.start_node = start_node
        self.target_node = target_node
        self.frontier = []
        self.dict_frontier = {}
        self.visited_nodes = []

    def run(self):
        starting_frontier_node = self._build_frontier_node(self.start_node, 0)
        self.frontier = [starting_frontier_node.node]
        self.dict_frontier = {
            starting_frontier_node.node: starting_frontier_node
        }
        self.visited_nodes = []
        resulting_frontier_node = self._iterate()
        if resulting_frontier_node:
            path_string = f'{resulting_frontier_node.path} with {resulting_frontier_node.total_distance} total distance'
        else:
            path_string = 'Does not exist'
        print(f'Path from {self.start_node} to {self.target_node}: {path_string}')

    def _build_frontier_node(
            self,
            node: str,
            distance_frontier_to_node: float,
            origin: Optional[FrontierNode] = None
    ) -> FrontierNode:
        total_distance = distance_frontier_to_node + origin.total_distance if origin else distance_frontier_to_node
        total_evaluation = total_distance + self.heuristics[node]

        path = origin.path.copy() if origin else []
        path.append(node)

        return FrontierNode(
            node=node,
            total_distance=total_distance,
            total_evaluation=total_evaluation,
            path=path
        )

    def _iterate(self) -> Optional[FrontierNode]:
        found_path = False
        resulting_frontier_node = None
        while len(self.frontier) > 0 and not found_path:
            current_frontier_node = self._pop_current_node()

            if current_frontier_node == self.target_node:
                found_path = True
                resulting_frontier_node = current_frontier_node

            else:
                for connection in self.connections[current_frontier_node.node]:
                    frontier_node = self._build_frontier_node(
                        connection['target'],
                        connection['distance'],
                        current_frontier_node
                    )

        return resulting_frontier_node

    def _pop_current_node(self) -> FrontierNode:
        current_node = self.frontier[0]
        self.frontier = self.frontier[1:]
        self.visited_nodes.append(current_node)
        return self.dict_frontier[current_node]

    def _add_node_to_frontier(self, frontier_node: FrontierNode):
        """
        Adds node to frontier.
        """
        if frontier_node.node not in self.visited_nodes:
            if frontier_node.node in self.dict_frontier.keys():
                if frontier_node.total_distance < self.dict_frontier[frontier_node.node].total_distance:
                    self.dict_frontier[frontier_node.node] = frontier_node
            else:
                self._insertion_sort(frontier_node)

    def _insertion_sort(self, frontier_node: FrontierNode):
        """
        Inserts a new FrontierNode on the frontier, in an ordered way.
        """
        self.dict_frontier[frontier_node.node] = frontier_node
        found = False
        index = 0
        while index < len(self.frontier) and not found:
            if self.dict_frontier[self.frontier[index]].total_evaluation > frontier_node.total_evaluation:
                self.frontier = self.frontier[:index] + [frontier_node.node] + self.frontier[index:]
                found = True

        if not found:
            self.frontier.append(frontier_node.node)


from typing import List
from typing import Optional

from src.data_structures.frontier_node import FrontierNode


class AStar:
    """
    Members:
        node_names: list of node names.
        connections:
            dict where each key has list of connections.
            Each connection is like { target: node_name, distance: float }
        heuristics: dict where each key (node name) is a float estimating the distance to the target node.
        start_node_name: starting node name.
        target_node_name: target node name.
        frontier: list of ordered node names, based on their evaluation to get to the target node.
        dict_frontier: a dict where each key (node name) is a FrontierNode, used for optimizing the search.
        visited_nodes: list of node names that were already visited.
    """

    def __init__(self, node_names: List[str], connections: dict, heuristics: dict, start_node: str, target_node: str):
        self.node_names = node_names
        self.connections = connections
        self.heuristics = heuristics
        self.start_node_name = start_node
        self.target_node_name = target_node
        self.ordered_frontier_node_names = []
        self.dict_frontier = {}
        self.visited_nodes = []

    def run(self) -> Optional[FrontierNode]:
        starting_frontier_node = self._build_frontier_node(self.start_node_name, 0)
        self.ordered_frontier_node_names = [starting_frontier_node.name]
        self.dict_frontier = {
            starting_frontier_node.name: starting_frontier_node
        }
        self.visited_nodes = []
        return self._iterate()

    def _build_frontier_node(
            self,
            node_name: str,
            distance_frontier_to_node: float,
            origin: Optional[FrontierNode] = None
    ) -> FrontierNode:
        total_distance = distance_frontier_to_node + origin.total_distance if origin else distance_frontier_to_node
        total_evaluation = total_distance + self.heuristics[node_name]

        path = origin.path.copy() if origin else []
        path.append(node_name)

        return FrontierNode(
            name=node_name,
            total_distance=total_distance,
            total_evaluation=total_evaluation,
            path=path
        )

    def _iterate(self) -> Optional[FrontierNode]:
        found_path = False
        resulting_frontier_node = None
        while len(self.ordered_frontier_node_names) > 0 and not found_path:
            current_frontier_node = self._pop_current_node()
            if self._is_final_node(current_frontier_node):
                found_path = True
                resulting_frontier_node = current_frontier_node
            else:
                self._add_node_connections_to_frontier(current_frontier_node)

        return resulting_frontier_node

    def _pop_current_node(self) -> FrontierNode:
        """
        Gets the first node on the frontier.
        """
        current_node = self.ordered_frontier_node_names[0]
        self.ordered_frontier_node_names = self.ordered_frontier_node_names[1:]
        self.visited_nodes.append(current_node)
        return self.dict_frontier[current_node]

    def _is_final_node(self, frontier_node: FrontierNode) -> bool:
        return frontier_node.name == self.target_node_name

    def _add_node_connections_to_frontier(self, frontier_node: FrontierNode):
        for connection in self.connections[frontier_node.name]:
            connection_frontier_node = self._build_frontier_node(
                connection['target'],
                connection['distance'],
                frontier_node
            )
            self._add_node_to_frontier(connection_frontier_node)

    def _add_node_to_frontier(self, frontier_node: FrontierNode):
        if self._is_node_visited(frontier_node):
            if self._is_new_path_to_node_closer_than_old_path(frontier_node):
                self._insertion_sort(frontier_node)
        else:
            if self._is_node_on_frontier(frontier_node):
                if self._is_new_path_to_node_closer_than_old_path(frontier_node):
                    self._update_node_on_frontier(frontier_node)
            else:
                self._insertion_sort(frontier_node)

    def _is_node_visited(self, frontier_node: FrontierNode) -> bool:
        return frontier_node.name in self.visited_nodes

    def _is_node_on_frontier(self, frontier_node) -> bool:
        return frontier_node.name in self.ordered_frontier_node_names

    def _is_new_path_to_node_closer_than_old_path(self, frontier_node: FrontierNode) -> bool:
        return frontier_node.total_distance < self.dict_frontier[frontier_node.name].total_distance

    def _update_node_on_frontier(self, frontier_node: FrontierNode):
        old_index = self.ordered_frontier_node_names.index(frontier_node.name)
        del self.ordered_frontier_node_names[old_index]
        self._insertion_sort(frontier_node)

    def _insertion_sort(self, frontier_node: FrontierNode):
        """
        Inserts a new FrontierNode on the frontier in an ordered way basing on the total_evaluation of the FrontierNode.
        """
        self.dict_frontier[frontier_node.name] = frontier_node
        found = False
        index = 0
        while index < len(self.ordered_frontier_node_names) and not found:
            current_frontier_node = self.dict_frontier[self.ordered_frontier_node_names[index]]
            if self._is_node_better_evaluated(frontier_node, current_frontier_node):
                found = True
                self._insert_node_on_index(index, frontier_node)
            index += 1

        if not found:
            self.ordered_frontier_node_names.append(frontier_node.name)

    @staticmethod
    def _is_node_better_evaluated(first_node: FrontierNode, second_node: FrontierNode) -> bool:
        # We use <= here because the lesser the evaluation, the better also the equals makes it easier for inserting on
        # 3 -> [3,3,3,3,3...] for example.
        return first_node.total_evaluation <= second_node.total_evaluation

    def _insert_node_on_index(self, index: int, frontier_node: FrontierNode):
        self.ordered_frontier_node_names = (
            self.ordered_frontier_node_names[:index] +
            [frontier_node.name] +
            self.ordered_frontier_node_names[index:]
        )

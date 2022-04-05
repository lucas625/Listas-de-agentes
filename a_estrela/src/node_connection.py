from src.node import Node


class NodeConnection:

    def __init__(self, target: Node, distance: int):
        self.target = target
        self.distance = distance

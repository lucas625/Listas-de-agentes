"""
Script for Q learning.
"""

import argparse

from learner import QLearner


def _arguments_definition():
    """
    Method for creating the possible parameters for execution.
    :return ArgumentParser:
    """
    parser = argparse.ArgumentParser(description='Runs the Q-learning.')
    parser.add_argument(
        '--number-of-episodes',
        default=5,
        type=int,
        help='The number of episodes (Default is 5).')
    parser.add_argument(
        '--number-of-evaluation-intervals',
        default=1,
        type=int,
        help='The number of evaluation intervals (Default is 1).')
    parser.add_argument(
        '--alpha',
        default=0.5,
        type=float,
        help='The learning rate (Default is 0.5).')
    parser.add_argument(
        '--gamma',
        default=1,
        type=float,
        help='The discount factor (Default is 1).')
    parser.add_argument(
        '--epsilon',
        default=0,
        type=float,
        help='The chance of performing a random action (Default is 0).')

    return parser.parse_args()


if __name__ == '__main__':
    args = _arguments_definition()

    learner = QLearner(args.number_of_episodes, args.alpha, args.gamma, args.epsilon)
    learner.learn()

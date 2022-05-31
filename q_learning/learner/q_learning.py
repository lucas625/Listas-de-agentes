"""
Module for learning with Q learn.
"""

import random
from typing import Optional

from environment.six_table import SixTable


class QLearner:
    """
    Class for controlling the Q learning.
    """

    def __init__(self, number_of_episodes, alpha, gamma, epsilon):
        """
        Class constructor.
        :param int number_of_episodes: the number of episodes.
        :param float alpha: the learning rate.
        :param float gamma: discount factor.
        :param float epsilon: chance of taking a random action.
        """
        self._env = SixTable()
        self._table = None
        self._number_of_episodes = number_of_episodes
        self._alpha = alpha
        self._gamma = gamma
        self._epsilon = epsilon

    def learn(self):
        """
        Q-Learning - TD Control
        """
        self._table = self._initialize_table()
        for episode_index in range(1, self._number_of_episodes + 1):
            self._iterate_episode(episode_index)
        print()

    def _initialize_table(self):
        return [[0 for _ in range(self._env.number_of_actions)] for _ in range(self._env.number_of_states)]

    def _iterate_episode(self, episode_index):
        """
        Perform the actions necessary for running the episode.
        :param int episode_index: the 1-based episode index.
        """
        print(f'----- Trajetória {episode_index} -----')
        print('Estado atual / Ação / Próximo estado')
        score = 0
        self._env.reset()  # start episode
        state_index = self._env.state_index
        done = False
        while not done:
            action_index = self._choose_action_by_epsilon_greedy(state_index)
            next_state_index, reward, done = self._env.step(action_index)
            print(f'{state_index} {self._env.get_action_by_index(action_index)} {next_state_index}')
            score += reward
            self._update_table(state_index, action_index, reward, next_state_index)
            state_index = next_state_index

        print('----- Printing table -----')
        self._env.print_actions()
        table_string = [
            f'State {index}: ' + ' '.join([str(state_action_reward) for state_action_reward in state_action_rewards]) for
            index, state_action_rewards in
            enumerate(self._table)
        ]
        print('\n'.join(table_string))

    def _choose_action_by_epsilon_greedy(self, state_index: int) -> int:
        """
        Selects epsilon-greedy action for supplied state.
        :return: the action index to be taken
        """
        if random.random() > self._epsilon:
            state_action_rewards = self._table[state_index - 1]
            max_reward = max(state_action_rewards)
            action_index = state_action_rewards.index(max_reward)
        else:
            action_index = random.randint(0, self._env.number_of_actions)
        return action_index

    def _update_table(self, state_index: int, action_index: int, reward: float, next_state_index: Optional[int] = None):
        """
        Updated table for the most recent experience.
        :param state_index: the current state.
        :param action_index: the current action.
        :param reward: the reward for the action:
        :param next_state_index: the next state.
        """
        current_estimation = self._table[state_index - 1][action_index]  # estimate in Q-table (for current state, action pair)
        next_state_value = max(self._table[next_state_index - 1]) if next_state_index is not None else 0
        target = reward + (self._gamma * next_state_value)  # construct TD target
        new_value = current_estimation + (self._alpha * (target - current_estimation))  # get updated value
        self._table[state_index - 1][action_index] = new_value

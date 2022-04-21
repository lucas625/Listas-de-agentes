import math
from copy import deepcopy
from typing import List

from src.helpers.print_helper import PrintHelper


class MinMax:
    RED_PLAYER = 'v'
    BLACK_PLAYER = 'p'

    def __init__(self, starting_state):
        self._starting_state = starting_state
        self.state = starting_state
        self.current_player = self.RED_PLAYER
        self.lines = len(self.state)
        self.columns = len(self.state[0])
        self.selected_plays = [self._starting_state]
        self.iteration_index = 0

    def run(self) -> List[List[List[str]]]:
        self.state = self._starting_state
        self.selected_plays = [self._starting_state]
        self.iteration_index = 0
        self._iterate()
        return self.selected_plays

    def _iterate(self):
        finished = False
        while not finished:
            if self.iteration_index == 11:
                print(10)
            if self._is_board_full():
                print('----- DRAW -----')
                return
            self.print(f'Player {self.current_player} is playing.')
            self.print(f'Current state:\n{PrintHelper.state_to_str(self.state)}')
            first_player_possible_plays = self._generate_possible_plays(self.state, self.current_player)
            self.print(f'Possible plays: {first_player_possible_plays}')
            second_player_possible_plays = []
            for first_player_possible_play in first_player_possible_plays:
                if self._has_player_won_on_state(first_player_possible_play, self.current_player) and not finished:
                    print(f'----- Player: {self.current_player} won -----')
                    print(f'Final state:\n{PrintHelper.state_to_str(first_player_possible_play)}')
                    self.selected_plays.append(first_player_possible_play)
                    finished = True
                else:
                    second_player_possible_plays.append(
                        self._generate_possible_plays(first_player_possible_play, self._get_next_player())
                    )
            if not finished:
                self.print(f'Next player possible plays: {second_player_possible_plays}')
                points = self._count_points(first_player_possible_plays, second_player_possible_plays)
                self.print(f'Possible plays\' points: {points}')
                self._update_state_based_on_points(first_player_possible_plays, points)

    def _get_next_player(self):
        return self.BLACK_PLAYER if self.current_player == self.RED_PLAYER else self.RED_PLAYER

    def _generate_possible_plays(self, state: List[List[str]], player: str):
        new_states = []
        for column_index in range(self.columns):
            if state[0][column_index] == '':
                new_state = self._create_state_by_pushing_on_column(state, player, column_index)
                new_states.append(new_state)
        return new_states

    def _create_state_by_pushing_on_column(self, state: List[List[str]], player: str, column: int) -> List[List[str]]:
        new_state = deepcopy(state)
        line_index = self.lines - 1
        found = False
        while (not found) and (line_index >= 0):
            if new_state[line_index][column] == '':
                new_state[line_index][column] = player
                found = True
            line_index -= 1
        return new_state

    def _count_points(self, plays: List[List[List[str]]], next_player_plays: List[List[List[List[str]]]]) -> List[int]:
        actions_points = []
        for (index, state) in enumerate(plays):
            if self._has_player_won_on_state(state, self.current_player):
                action_points = math.inf  # There is no case where the red player plays and black player wins
            else:
                action_points = 0
                next_player = self._get_next_player()
                for next_player_play_state in next_player_plays[index]:
                    if self._has_player_won_on_state(next_player_play_state, next_player):
                        action_points -= 1  # There is no case where the black player plays and red player wins
                        # Here we consider -1 even if the red player is the next player
                        # It is the same logic as conventional min-max, but we can see it as max-max
                        # (from each player perspective)

            actions_points.append(action_points)
        return actions_points

    def _has_player_won_on_state(self, state: List[List[str]], player: str) -> bool:
        won = self._has_player_won_on_state_horizontal(state, player)
        if not won:
            won = self._has_player_won_on_state_vertical(state, player)
        if not won:
            won = self._has_player_won_on_state_diagonal(state, player)
        return won

    def _has_player_won_on_state_horizontal(self, state: List[List[str]], player: str) -> bool:
        won = False
        line_index = 0
        column_index = 0
        while (line_index < self.lines) and not won:
            while (column_index < self.columns - 2) and not won:
                all_equal = True
                for index in range(3):
                    if not (state[line_index][column_index + index] == player):
                        all_equal = False
                if all_equal:
                    won = True
                column_index += 1
            line_index += 1
        return won

    def _has_player_won_on_state_vertical(self, state: List[List[str]], player: str) -> bool:
        won = False
        line_index = 0
        column_index = 0
        while (column_index < self.columns) and not won:
            while (line_index < self.lines - 2) and not won:
                all_equal = True
                for index in range(3):
                    if not (state[line_index + index][column_index] == player):
                        all_equal = False
                if all_equal:
                    won = True
                line_index += 1
            column_index += 1
        return won

    def _has_player_won_on_state_diagonal(self, state: List[List[str]], player: str) -> bool:
        won = self._has_player_won_on_state_increasing_diagonal(state, player)
        if not won:
            won = self._has_player_won_on_state_decreasing_diagonal(state, player)
        return won

    def _has_player_won_on_state_increasing_diagonal(self, state: List[List[str]], player: str) -> bool:
        won = False
        line_index = 0
        column_index = 0
        while (line_index < self.lines - 2) and not won:
            while (column_index < self.columns - 2) and not won:
                all_equal = True
                for index in range(3):
                    if not (state[line_index + index][column_index + index] == player):
                        all_equal = False
                if all_equal:
                    won = True
                column_index += 1
            line_index += 1
        return won

    def _has_player_won_on_state_decreasing_diagonal(self, state: List[List[str]], player: str) -> bool:
        won = False
        line_index = self.lines - 1
        column_index = self.columns - 1
        while (line_index >= 2) and not won:
            while (column_index >= 2) and not won:
                all_equal = True
                for index in range(3):
                    if not (state[line_index - index][column_index - index] == player):
                        all_equal = False
                if all_equal:
                    won = True
                column_index -= 1
            line_index -= 1
        return won

    def _update_state_based_on_points(self, possible_plays: List[List[List[str]]], points: List[int]):
        max_index = 0
        for index in range(len(points)):
            if points[max_index] < points[index]:
                max_index = index
        self.state = possible_plays[max_index]
        self.selected_plays.append(self.state)
        self.current_player = self._get_next_player()
        self.iteration_index += 1

    def _is_board_full(self) -> bool:
        is_full = True
        for column_index in range(self.columns):
            if self.state[0][column_index] == '':
                is_full = False
        return is_full

    def print(self, string: str):
        print(f'{self.iteration_index} - {string}')

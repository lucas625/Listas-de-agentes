class SixTable:
    _DOWN = 'DOWN'
    _UP = 'UP'
    _RIGHT = 'RIGHT'
    _LEFT = 'LEFT'

    def __init__(self):
        self._actions = [SixTable._UP, SixTable._DOWN, SixTable._LEFT, SixTable._RIGHT]
        self._states = [[5, 6], [3, 4], [1, 2]]
        self._state = [2, 0]
        self._target = [0, 1]

    @property
    def number_of_actions(self):
        return 4

    @property
    def number_of_states(self):
        return 6

    @property
    def state_index(self):
        return self._states[self._state[0]][self._state[1]]

    def get_action_by_index(self, action_index: int):
        return self._actions[action_index]

    def reset(self):
        self._state = [2, 0]

    def step(self, action_index: int):
        action = self._actions[action_index]
        hit_wall = False

        if action == SixTable._DOWN:
            if self._state[0] == 2:
                hit_wall = True
            else:
                self._state[0] = self._state[0] + 1
        elif action == SixTable._UP:
            if self._state[0] == 0:
                hit_wall = True
            else:
                self._state[0] = self._state[0] - 1
        elif action == SixTable._LEFT:
            if self._state[1] == 0:
                hit_wall = True
            else:
                self._state[1] = self._state[1] - 1
        elif action == SixTable._RIGHT:
            if self._state[1] == 2:
                hit_wall = True
            else:
                self._state[1] = self._state[1] + 1

        done = self._is_done()
        if done:
            reward = 10
        elif hit_wall:
            reward = -10
        else:
            reward = -1
        return self.state_index, reward, done

    def _is_done(self):
        return self._state == self._target

    def print_actions(self):
        print('Actions: ' + ' '.join(self._actions))

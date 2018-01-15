import gym.spaces
import gym.wrappers
import numpy as np


def concat_states(state):
    history = state["history"]
    weights = np.array([np.squeeze(state["weights"])])
    acc = np.array(state["acc"])
    state = np.concatenate([weights, history, acc])
    return state


class ConcatStates(gym.Wrapper):
    """
    Concat both state arrays for models that take a single inputs.

    Usage:
        env = ConcatStates(env)

    Ref: https://github.com/openai/gym/blob/master/gym/wrappers/README.md
    """

    def __init__(self, env):
        super(ConcatStates, self).__init__(env)
        hist_space = self.observation_space.spaces["history"]
        hist_shape = hist_space.shape
        self.observation_space = gym.spaces.Box(-10, 10, shape=(hist_shape[0] + 2))

    def step(self, action):

        state, reward, done, info = self.env.step(action)

        # concat the two state arrays, since some models only take a single output
        state = concat_states(state)

        return state, reward, done, info

    def reset(self):
        state = self.env.reset()
        return concat_states(state)

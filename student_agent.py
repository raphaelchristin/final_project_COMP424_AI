# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
from constants import *
from copy import deepcopy
import numpy as np
import sys
from agents.MonteCarlo import MonteCarlo
import time


@register_agent("student_agent")
class StudentAgent(Agent):
    """
    A dummy class for your implementation. Feel free to use this class to
    add any helper functionalities needed for your agent.
    """

    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "StudentAgent"
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }
        self.autoplay = True #enable autoplay
        self.monte_carlo = None #initialize 

    def step(self, chess_board, my_pos, adv_pos, max_step):
        """
        Implement the step function of your agent here.
        You can use the following variables to access the chess board:
        - chess_board: a numpy array of shape (x_max, y_max, 4)
        - my_pos: a tuple of (x, y)
        - adv_pos: a tuple of (x, y)
        - max_step: an integer

        You should return a tuple of ((x, y), dir),
        where (x, y) is the next position of your agent and dir is the direction of the wall
        you want to put on.

        Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
        """
        if self.monte_carlo is None:
            self.monte_carlo = MonteCarlo(chess_board, my_pos, adv_pos, max_step)#create monteCarlo object if not present

        move = self.monte_carlo.get_move(chess_board, my_pos, adv_pos)
        return move #self.monte_carlo.get_move(chess_board, my_pos, adv_pos)#return move from monte carlo


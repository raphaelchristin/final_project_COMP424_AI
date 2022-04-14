from datetime import timedelta
from datetime import datetime
from agents.utilities import *
from random import choice
from copy import deepcopy
from math import log, sqrt

"""
Code adapted from http://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/
MonteCarlo Algorithm for the game playing
"""
class MonteCarlo:
    def __init__(self,chess_board, my_pos, adv_pos, max_step, **kwargs):
        #self.states = []#store encountered states
        self.max_step = max_step
        self.chess_board = chess_board
        self.my_pos = my_pos
        self.adv_pos = adv_pos

        sec = kwargs.get("time", 1.95)
        self.calculation_time = timedelta(seconds=sec) #time llowed for calculation
        self.setup = True #setup allows for more computation time, true until updated after the first computation
        self.max_moves = kwargs.get("max_moves", 50) #max moves for simulations
        self.C = kwargs.get("C", 1.4) #constant for confidence interval 
        self.wins = {} #store number of wins for each state
        self.plays ={} #store number of plays for each state
        self.num = 0 #move count

    def get_move(self, board, my_pos, adv_pos):
        """returns a move from the algorithm, the one with the best stats
        """
        self.num += 1 #one more move from the adv
        player = True #player is true or false, True when get move is called
        self.adv_pos = adv_pos#update values
        self.my_pos = my_pos
        self.chess_board = board
        moves = get_moves(self.chess_board, self.my_pos, self.adv_pos, self.max_step)#get list of random moves
        start = datetime.utcnow()
        if self.setup:
            time = timedelta(seconds = 29.95)#allow longer computation at setup
            self.setup=False
        else :
            time = self.calculation_time

        while datetime.utcnow() - start < time:#simulate until the time limit
            self.run_simulation()

        moves_states = [(play, (play, self.num)) for play in moves]#pack moves and states together

        move,S = moves_states[0]
        percent = self.wins.get((player,S), 0)/self.plays.get((player, S), 1)

        for p, S in moves_states[1:]:#update best move and state
            if self.wins.get((player,S), 0)/self.plays.get((player, S), 1) > percent:
                move = p
                percent = self.wins.get((player,S), 0)/self.plays.get((player, S), 1)

        self.num += 1#one more move
        return move

    def run_simulation(self):
        """runs simulations. Expands one state and adds it to the plays and wins dictionaries. 
        Chooses moves based on current statistics or at random if not possible.
        updates the statistics if a winner is reached.
        """

        visited_states = set() #store visited stated in this simulation
        player = True#start with our player
        num = self.num #store locally for faster lookup
        board = deepcopy(self.chess_board)
        pos = self.my_pos
        adv = self.adv_pos
        max_step = self.max_step
        plays, wins = self.plays, self.wins
        winner = None#winner is none until there is one

        expand = True
        for t in range(self.max_moves):#simulate until max_moves
            moves = get_moves(board, pos, adv, max_step)
            moves_states = [(play, (play, num)) for play in moves]

            if all(plays.get((player, S)) for p, S in moves_states):#if all the moves have already considered, base the next play on the stats
                log_total = log(sum(plays[(player, S)] for p,S in moves_states))

                value = 0
                play, state = moves_states[0]

                for p,S in moves_states[1:]:#find maximum
                    v = (wins[(player, S)]/plays[(player, S)])+self.C*sqrt(log_total/plays[(player, S)])#UCT calculation
                    if v > value:
                        value = v
                        play = p
                        state = S

            else: 
                play, state = choice(moves_states)

            
            move,dir = play
            r,c = move
            board = apply_move(board, r,c,dir)#apply the move 
            
            if expand and (player, state) not in self.plays:#expand only one state
                expand = False
                self.plays[(player, state)] = 0#add to plays and wins
                self.wins[(player, state)] = 0
                
            visited_states.add((player, state))

            win, score = check_win(board, pos, adv)
            if win:
                if score == 1:
                    winner = player
                else:
                    winner = not player#break if win, store the winner
                break
            
            pos = adv#update for next loop, different player so we reverse
            adv = move
            player = not player
            num += 1

        for player, state in visited_states:#update plays and wins if necessary
            if (player, state) not in self.plays:
                continue
            self.plays[(player, state)] += 1
            if winner is not None:
                if player == winner:
                    self.wins[(player, state)]+= 1
            
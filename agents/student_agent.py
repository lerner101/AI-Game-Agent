from agents.agent import Agent
from store import register_agent
import random
from collections import deque
import sys
import numpy as np
from copy import deepcopy
import time


@register_agent("student_agent")
class StudentAgent(Agent):

    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "Patient Paul"
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }

    def step(self, chess_board, my_pos, adv_pos, max_step):
        # Define the initial depth for the minimax algorithm
        initial_depth = 4

        # Setting max allowed time for the minimax algorithm so moves dont go over the time limit
        max_time_seconds = 1.79
        start_time = time.time()

        # Initialize the best move and wall placement
        best_eval, best_move, best_wall_placement = float('-inf'), None, None

        # Perform iterative deepening until the maximum depth is reached
        # This always ends up stopping when max time is reached
        for depth in range(1, 4):
            eval, move, wall_placement = self.minimax(
                chess_board, my_pos, adv_pos, max_step, depth, True, start_time, max_time_seconds
            )

            
            if eval > best_eval:
                best_eval, best_move, best_wall_placement = eval, move, wall_placement

            # At the end of a loop always checking the time
            if time.time() - start_time >= max_time_seconds:
                break

        return best_move, best_wall_placement

    
    def minimax(self, chess_board, my_pos, adv_pos, max_step, depth, is_maximizing_player, start_time, max_time_seconds):
        #Base case
        if depth == 0 or self.terminal_state_reached(chess_board, my_pos, adv_pos):
            return self.evaluate(chess_board, my_pos, adv_pos, max_step), None, None

        #Deciding move for the max player
        if is_maximizing_player:
            #Initialize values
            max_eval = float('-inf')
            best_move = None
            best_wall_placement = None
            #Call helper function to get all possible moves and iterate through each of them
            moves = self.get_all_possible_moves(chess_board, my_pos, max_step, adv_pos)
            if not moves:
                # No valid moves available
                return 0, my_pos, None
            for move in self.get_all_possible_moves(chess_board, my_pos, max_step, adv_pos):
                if time.time() - start_time >= max_time_seconds:
                    break
                #Call simulate with move to get new board, new position and best wall placement in that position
                new_board, new_my_pos, wall_placement = self.simulate(chess_board, my_pos, move, adv_pos, max_step)
                #Recursive call
                eval, _, _ = self.minimax(new_board, new_my_pos, adv_pos, max_step, depth - 1, False, start_time, max_time_seconds)
                #Checking if returned value is better than current best. If so update all values
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                    best_wall_placement = wall_placement

            return max_eval, best_move, best_wall_placement
        #Similar process above below, but now for min player
        else:
            min_eval = float('inf')
            best_move = None
            best_wall_placement = None
            moves = self.get_all_possible_moves(chess_board, my_pos, max_step, adv_pos)
            

            for move in moves:
                if time.time() - start_time >= max_time_seconds:
                    break
                new_board, new_my_pos, wall_placement = self.simulate(chess_board, my_pos, move, adv_pos, max_step)
                eval, _, _ = self.minimax(new_board, new_my_pos, adv_pos, max_step, depth - 1, True, start_time, max_time_seconds)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                    best_wall_placement = wall_placement

            return min_eval, best_move, best_wall_placement

    
    def terminal_state_reached(self, chess_board, my_pos, adv_pos):
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        r, c = my_pos
        allowed_dirs_my = [ d                                
                for d in range(0,4)                           # always 4 moves possible
                if not chess_board[r,c,d] and                 # know that chess_board true == wall
                not adv_pos == (r+moves[d][0],c+moves[d][1])] # cant go through opponent

        #Check for opponent as well:
        a, b = adv_pos
        allowed_dirs_adv = [ d                                
                for d in range(0,4)                           # same logic as above
                if not chess_board[a,b,d] and                 
                not my_pos == (a+moves[d][0],b+moves[d][1])]

        if len(allowed_dirs_my)==0 or len(allowed_dirs_adv)==0:
            return True
        else:
            return False


    #Evaluation functions, used to give a numerical value to potential moves and these values are uesed in minimax

    def evaluate(self, chess_board, my_pos, adv_pos,max_step):
        # Implementing an evaluation function
        
        board_size = (max_step*2)**2
        evaluation = []
        
        #Heuristic #1: Avoid near walls/corners
        wall_count = 0 #Red wall
        for d in range(4):
            r, c = my_pos

            if chess_board[r,c,d]: #if there is a wall
                wall_count +=1

        
        evaluation.append(((4 - wall_count)/4)*100)


        #Heuristic #2: How many squares are accessible if we move there
        #call get_all_possible_moves.
        #take a % of the possible moves (% board size)
        possible_moves = len(self.get_all_possible_moves(chess_board, my_pos,max_step,adv_pos))
        possible_moves_adv = len(self.get_all_possible_moves(chess_board, adv_pos,max_step,my_pos))

        evaluation.append((possible_moves/board_size)*100)
        evaluation.append(((board_size - possible_moves_adv)/board_size)*100)

        #print(evalFinal/len(evaluation))

        return (sum(evaluation)/len(evaluation))
    
    def evaluate_wall(self,chess_board,move,adv_pos, max_steps):
        #Seperate evaluation function to determine wall placement
        r, c = move
        allowed_barriers = [i for i in range(4) if not chess_board[r, c, i]]

        best_option = -1000
        selected_wall = 0

        for selection in allowed_barriers:
            newBoard = self.simulate_with_wall(chess_board, move, selection)

            #Get all possible moves of the opponent
            adv_options = len(self.get_all_possible_moves(newBoard, adv_pos, max_steps, move))

            our_options = len(self.get_all_possible_moves(newBoard, move, max_steps, adv_pos))
            #Want the biggest difference in terms of move options for us vs them
            
            adv_wall_count = 0 #Red wall
            for d in range(4):
                r, c = move

            if newBoard[r,c,d]: #if there is a wall
                adv_wall_count +=1
            

            ranking = our_options - adv_options
            if best_option < ranking:
                best_option = ranking
                selected_wall = selection
            
        return selected_wall

    def update_move(self, pos, move):
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        m_r, m_c = moves[move]
        return pos[0] + m_r, pos[1] + m_c



    #Helper function - returns all possible moves for given starting position
    def get_all_possible_moves(self, chess_board, start_pos, max_steps, adv_pos):
        #Move directions from other files
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        visited = set()
        queue = deque([(start_pos, 0)])

        #Current position is always a viable move so add it right away
        possible_moves = [start_pos]

        while queue:
            current_position, steps = queue.popleft()

            if steps >= max_steps:
                break

            for move_index, move in enumerate(moves):
                new_position = self.update_move(current_position, move_index)

                # First check: new position has to be within boundaries
                if not (0 <= new_position[0] < chess_board.shape[0] and 0 <= new_position[1] < chess_board.shape[1]):
                    continue

                # Second check: check if there is a wall in the direction of the move
                if chess_board[current_position[0], current_position[1], move_index]:
                    continue

                # Third check: check if there is a wall behind the direction of the move
                opposite_move_index = (move_index + 2) % 4
                if chess_board[new_position[0], new_position[1], opposite_move_index]:
                    continue

                # Fourth check: check if we are going through the opponent
                if new_position == adv_pos:
                    continue

                #If it gets through all the checks, then lets add it to the possible moves
                if new_position not in visited:
                    visited.add(new_position)
                    queue.append((new_position, steps + 1))
                    possible_moves.append(new_position)

        return possible_moves
    

    #Simulation functions - Simulating playing a move and updates the chessboard so we can evaluate the move beforehand 
    def simulate(self, chess_board, pos, move,adv_pos, max_steps):
            # simulate a new move with a new board
            newBoard = deepcopy(chess_board)
            r, c = move
            # Choose where to put the new barrier
            allowed_barriers = [i for i in range(4) if not chess_board[r, c, i]]
            assert len(allowed_barriers) >= 1
            wall_placement = self.evaluate_wall(chess_board,move,adv_pos, max_steps)
            newBoard[r, c, wall_placement] = True
            return newBoard, (r,c), wall_placement
    
    def simulate_with_wall(self, chess_board, move, wall_placement):
            # simulate a new move with a new board
            newBoard = deepcopy(chess_board)
            r, c = move
            newBoard[r, c, wall_placement] = True
            return newBoard
    



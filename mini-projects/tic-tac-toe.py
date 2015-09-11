"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
def mc_trial(board, player):
    """Play a complete game and
    update the board"""
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        next_move = random.choice(empty_squares)
        board.move(next_move[0], next_move[1], player)
        player = provided.switch_player(player)
        
def mc_update_scores(scores, board, player): 
    """update score according to board state
    """
    winner = board.check_win()
    if winner == provided.DRAW:
        return
    
    other_player = provided.switch_player(player)
    dim = board.get_dim()
    for row in xrange(dim):
        for col in xrange(dim):
            grid_state = board.square(row, col)
            #current player is winner
            if winner == player:
                if grid_state == player:
                    scores[row][col] += SCORE_CURRENT
                elif grid_state == other_player:
                    scores[row][col] -= SCORE_OTHER
            #current player is loser
            else:
                if grid_state == player:
                    scores[row][col] -= SCORE_CURRENT
                elif grid_state == other_player:
                    scores[row][col] += SCORE_OTHER

def get_best_move(board, scores):
    """return next move according to
    board state and score"""
    empty = board.get_empty_squares()
    if len(empty) == 0:
        return
    
    vals = [scores[square[0]][square[1]] for square in empty]
    max_val = max(vals)
    moves = []
    
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if scores[row][col] == max_val and ((row, col) in empty):
                moves.append((row, col))
    
    best_move = moves[random.randrange(len(moves))]
    return best_move
    
def mc_move(board, player, trials):
    """Performs a number of monte carlo
    trials and return the best next move
    """
    dim = board.get_dim()
    scores = [[0 for dummycol in range(dim)] 
              for dummyrow in range(dim)]
    for dummy_i in xrange(trials):
        original_board = board.clone()
        mc_trial(original_board, player)
        mc_update_scores(scores, original_board, player)
    return get_best_move(board, scores)



# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

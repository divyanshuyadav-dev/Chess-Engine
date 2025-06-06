import time
from .chess import Chess_State

class Engine:

    def __init__(self):
        # Initialize tracking variables and transposition table
        self.principle_list = []
        self.branch = 0
        self.pruned = 0
        self.transposition_table = {}
        self.hit = 0
        self.node_cnt = 0

    def get_principle_list(self):
        # Return principle variation if available
        if len(self.principle_list) == 0:
            raise Exception("Please use 'get_best_move' function to set the game state")
        return self.principle_list

    def get_best_move(self, state: Chess_State, depth, is_white_move: bool):
        # Reset stats for new search
        self.branch = self.pruned = self.hit = self.node_cnt = 0
        score, move = self.__minimax(state, depth, is_white_move, -float('inf'), float('inf'))
        return move

    def get_best_move_iterative(self, state: Chess_State, max_depth, is_white_move: bool, time_limit=3.0):
        best_move = None
        self.branch = self.pruned = self.hit = self.node_cnt = 0
        self.transposition_table.clear()

        self.start_time = time.perf_counter()
        self.time_limit = time_limit

        for depth in range(1, max_depth + 1):
            # Check if we've run out of time
            if time.perf_counter() - self.start_time > self.time_limit:
                break
            score, move = self.__minimax(state, depth, is_white_move, -float('inf'), float('inf'))
            if move:
                best_move = move

        return best_move

    def __minimax(self, state: Chess_State, depth, is_maximising, alpha, beta):
        # Count total nodes visited
        self.node_cnt += 1
        alpha_orig = alpha

        # Terminal condition: switch to quiescence search
        if depth == 0:
            return self.quiescence_search(state, alpha, beta, is_maximising), None

        best_score = -float('inf') if is_maximising else float('inf')
        best_move = None

        # Order moves to maximize pruning potential
        all_moves = state.get_all_valid_moves(is_maximising)

        for move in all_moves:
            sr, sc, er, ec = move
            move_obj = state.make_move(sr, sc, er, ec)

            # # Transposition table lookup
            # key = state.compute_zobrist_hash()
            # tt_key = (key, is_maximising)

            # if tt_key in self.transposition_table:
            #     tt_score, flag, tt_depth = self.transposition_table[tt_key]
            #     if tt_depth >= depth:
            #         self.hit += 1
            #         if flag == 'EXACT':
            #             score = tt_score
            #         elif flag == 'LOWERBOUND':
            #             score = tt_score
            #             alpha = max(alpha, tt_score)
            #         elif flag == 'UPPERBOUND':
            #             score = tt_score
            #             beta = min(beta, tt_score)
            #         if alpha >= beta:
            #             state.undo_move(move_obj)
            #             self.pruned += 1
            #             return score, None
            #     else:
            #         self.branch += 1
            #         score, _ = self.__minimax(state, depth - 1, not is_maximising, alpha, beta)
            # else:
            self.branch += 1
            score, _ = self.__minimax(state, depth - 1, not is_maximising, alpha, beta)


            state.undo_move(move_obj)

            # Update best score and alpha-beta window
            if is_maximising:
                if score > best_score:
                    best_score = score
                    best_move = move_obj
                    alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score = score
                    best_move = move_obj
                    beta = min(beta, best_score)

            # Alpha-beta pruning condition
            if alpha >= beta:
                self.pruned += 1
                break

        # Store result in transposition table with appropriate flag
        # flag = 'EXACT'
        # if best_score <= alpha_orig:
        #     flag = 'UPPERBOUND'
        # elif best_score >= beta:
        #     flag = 'LOWERBOUND'
        # self.transposition_table[(state.compute_zobrist_hash(), is_maximising)] = (best_score, flag, depth)

        return best_score, best_move

    def quiescence_search(self, state: Chess_State, alpha, beta, is_white_turn, depth=4):
        # Basic depth limit
        if depth == 0:
            return state.evaluate_board()

        eval = state.evaluate_board()

        # Stand-pat check
        if is_white_turn:
            if eval >= beta:
                return beta
            if alpha < eval:
                alpha = eval
        else:
            if eval <= alpha:
                return alpha
            if beta > eval:
                beta = eval

        # Generate only capture moves for quiescence search
        all_moves = state.get_all_valid_moves(is_white_turn)
        capture_moves = []
        for move in all_moves:
            sr, sc, er, ec = move
            if state.board[er][ec] != '--':
                capture_moves.append(move)

        ordered_moves = state.get_all_valid_moves_as_ordered(capture_moves)

        # Evaluate captures recursively
        for move in ordered_moves:
            sr, sc, er, ec = move
            move_obj = state.make_move(sr, sc, er, ec)
            score = -self.quiescence_search(state, -beta, -alpha, not is_white_turn, depth - 1)
            state.undo_move(move_obj)

            if is_white_turn:
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
            else:
                if score <= alpha:
                    return alpha
                if score < beta:
                    beta = score

        return alpha if is_white_turn else beta

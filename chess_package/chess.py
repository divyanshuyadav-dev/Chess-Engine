import copy
import random
from .move import Move

class Chess_State:

    PIECE_VALUES = {
        'P':1,
        'N':3,
        'B':3,
        'R':5,
        'Q':9,
        'K':1000 # most valueable piece
    }

    # Piece Square Table
    PST = {
        'P': [
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 5,  5,  5, -5, -5,  5,  5,  5],
            [ 1,  1,  2,  3,  3,  2,  1,  1],
            [ 0,  0,  1,  4,  4,  1,  0,  0],
            [ 0,  0,  1,  4,  4,  1,  0,  0],
            [ 1,  1,  2,  3,  3,  2,  1,  1],
            [ 5,  5,  5, -5, -5,  5,  5,  5],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
        ],
        'N': [
            [-5, -4, -3, -3, -3, -3, -4, -5],
            [-4, -2,  0,  0,  0,  0, -2, -4],
            [-3,  0,  1,  1.5, 1.5, 1,  0, -3],
            [-3,  0.5, 1.5, 2,  2,  1.5, 0.5, -3],
            [-3,  0,  1.5, 2,  2,  1.5, 0, -3],
            [-3,  0.5, 1,  1.5, 1.5, 1,  0.5, -3],
            [-4, -2,  0,  0.5, 0.5, 0, -2, -4],
            [-5, -4, -3, -3, -3, -3, -4, -5],
        ],
        'B': [
            [-2, -1, -1, -1, -1, -1, -1, -2],
            [-1,  0,  0,  0,  0,  0,  0, -1],
            [-1,  0,  0.5, 1,  1,  0.5, 0, -1],
            [-1,  0.5, 0.5, 1,  1,  0.5, 0.5, -1],
            [-1,  0,  1,  1,  1,  1,  0, -1],
            [-1,  1,  1,  1,  1,  1,  1, -1],
            [-1,  0.5, 0,  0,  0,  0, 0.5, -1],
            [-2, -1, -1, -1, -1, -1, -1, -2],
        ],
        'R': [
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0.5, 1,  1,  1,  1,  1,  1, 0.5],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0.5, 0.5, 0,  0,  0],
            [ 0,  0,  0,  0.5, 0.5, 0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0.5, 1,  1,  1,  1,  1,  1, 0.5],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
        ],
        'Q': [
            [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
            [-1,  0,  0,  0,  0,  0,  0, -1],
            [-1,  0,  0.5, 0.5, 0.5, 0.5,  0, -1],
            [-0.5,  0,  0.5, 0.5, 0.5, 0.5,  0, -0.5],
            [ 0,  0,  0.5, 0.5, 0.5, 0.5,  0, -0.5],
            [-1,  0.5, 0.5, 0.5, 0.5, 0.5,  0, -1],
            [-1,  0,  0.5, 0,  0,  0,  0, -1],
            [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
        ],
        'K': [  # Middle-game king safety
            [-6, -8, -8, -10, -10, -8, -8, -6],
            [-6, -8, -8, -10, -10, -8, -8, -6],
            [-6, -8, -8, -10, -10, -8, -8, -6],
            [-6, -8, -8, -10, -10, -8, -8, -6],
            [-4, -6, -6, -8, -8, -6, -6, -4],
            [-2, -4, -4, -4, -4, -4, -4, -2],
            [ 2,  2,  0,  0,  0,  0,  2,  2],
            [ 4,  4,  2,  0,  0,  2,  4,  4],
        ],
    }

    # to induce zobrist hashing
    ZOBRIST_TABLE = [[[random.getrandbits(64) for _ in range(12)] for _ in range(8)] for _ in range(8)]
    PIECE_TO_INDEX = {
        'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
        'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11,
    }

    
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]

        # track whether eligible for castling or not
        self.castling_rights = {
            'w': {'K': True, 'Q': True},
            'b': {'K': True, 'Q': True}
        }

        self.castled_dict ={
            'w':False,
            'b':False
        }

        # track the moevment of king
        self.king_positions = {'w': (7, 4), 'b': (0, 4)}  # Starting positions




    def print_board(self):
        for i, row in enumerate(self.board):
            # print file names
            if i == 0:
                files = [chr(97+i) for i in range(8)]
                print("  ", "  ".join(files))
            print(f"{8 - i}  {' '.join(row)}  {8 - i}")
            # print file names
            if i == 7:
                files = [chr(97+i) for i in range(8)]
                print("  ", "  ".join(files))


    # evaluate board based on the pieces count
    def evaluate_board(self):
    #+ve -> white has more advantage and vice-versa
        return (
            self.get_material_score() +
            self.get_positional_score() +
            self. get_mobility_score() + 
            self.get_castling_bonus()
        )
    # TODO: improve board evaluation logic (eg position in center, piece development etc)

    def get_material_score(self):
        score = 0
        for row in range(8):
            for col in range(8):
                # idetify piece
                piece = self.board[row][col]
                # skip when no piece is on current position
                if piece == '--':
                    continue
                color = piece[0]
                piece_type = piece[1]
                piece_value = self.PIECE_VALUES.get(piece_type, 0)
                # inc score if white and dec score if black
                score += piece_value  if color == 'w' else - piece_value
        return score
    
    def get_positional_score(self):
        score = 0
        for row in range(8):
            for col in range(8):
                # idetify piece
                piece = self.board[row][col]
                # skip when no piece is on current position
                if piece == '--':
                    continue
                color = piece[0]
                piece_type = piece[1]
                # add positional bonuses
                if piece_type in self.PST:
                    pst_row = row if color =='w' else 7-row # this help to mirror vales for black also
                    pst_score = self.PST[piece_type][pst_row][col]
                    score += pst_score if color == 'w' else  -pst_score
        return score
    
    def get_mobility_score(self):
        score = 0
        # more no of available moves means more advantage
        white_moves_count = self.get_all_valid_moves(True)
        black_moves_count = self.get_all_valid_moves(False)
        score += 0.1 * (len(white_moves_count) - len(black_moves_count))
        return score
    
    def get_castling_bonus(self):
        score = 0
        # add castling bonus
        for color in ['w', 'b']:
            if self.castling_rights[color]['K'] or self.castling_rights[color]['Q']:
                score += 10 if color == 'w' else -10
            if self.castled_dict.get(color, False):
                score += 30 if color == 'w' else -30
        return score
    

    def make_move(self, start_row, start_col, end_row, end_col):
        captured = False
        checked = False
        promoted = False
        castled = False
        moving_piece = self.board[start_row][start_col]
        captured_piece = self.board[end_row][end_col]
        prev_rights = copy.deepcopy(self.castling_rights)

        # actual motion
        self.board[end_row][end_col] = moving_piece
        self.board[start_row][start_col] = '--'

        if captured_piece != '--':
            captured = True

        # check if pawn reach at the back rank then promote
        if moving_piece[1] == 'P' and ( (end_row == 0 and moving_piece[0] == 'w') or (end_row == 7 and moving_piece[0] == 'b') ):
            self.board[end_row][end_col] = moving_piece[0]+'Q'
            promoted = True
        
        # restrict castling if king moved
        if moving_piece[1] == 'K':
            self.castling_rights[moving_piece[0]]['K'] = False
            self.castling_rights[moving_piece[0]]['Q'] = False
            # track the king motion
            self.king_positions[moving_piece[0]] = (end_row, end_col)
        # restrict casting to one side if that side rook moved
        if moving_piece[1] == 'R':
            if start_col == 0: # queen side a-file
                self.castling_rights[moving_piece[0]]['Q'] = False
            if start_col == 7: # king side h-file
                self.castling_rights[moving_piece[0]]['K'] = False
        

        # TODO: uncomment when you imp restrict castling when pieces are between king and rook
        # move rook when castling
        if moving_piece[1] == 'K' and abs(start_col - end_col) == 2:
            # track the king motion
            self.king_positions[moving_piece[0]] = (end_row, end_col)
            self.castled_dict[moving_piece[0]] = True
            if end_col == 6:  # kingside
                self.board[end_row][5] = self.board[end_row][7]
                self.board[end_row][7] = '--'
                castled = True
            elif end_col == 2:  # queenside
                self.board[end_row][3] = self.board[end_row][0]
                self.board[end_row][0] = '--'
                castled = True

        return Move(start_row, start_col, end_row, end_col, moving_piece, captured_piece, checked, promoted, captured, castled, prev_rights)
    

    def undo_move(self, move: Move):
        self.castling_rights = move.prevCastlingRight
        if move.isPromoted:
            # undo the pawn promotion
            self.board[move.start_row][move.start_col] = move.moved_piece
            self.board[move.end_row][move.end_col] = move.captured_piece
        else:
            # place moving peice at its prev position
            self.board[move.start_row][move.start_col] = move.moved_piece
            # place the captured piece (or space) back to its prev position
            self.board[move.end_row][move.end_col] = move.captured_piece

            if move.moved_piece[1] == 'K':
                # track the the king undo move
                self.king_positions[move.moved_piece[0]] = (move.start_row, move.start_col)
                #in case of being castled by king
                if move.hasCastled:
                    self.castled_dict[move.moved_piece[0]] = False
                    # replace rook to its origin position if castled
                    if move.end_col == 6: # king was castled king-side
                        self.board[move.end_row][7] = self.board[move.end_row][5]  
                        self.board[move.end_row][5] = "--"
                    elif move.end_col == 2: # king was castled queen side
                        self.board[move.end_row][0] = self.board[move.end_row][3]
                        self.board[move.end_row][3] = "--"


    def get_all_pseudo_legal_captures(self, is_white_turn):
        color = 'w' if is_white_turn else 'b'
        captures = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != '--' and piece[0] == color:
                    for tr, tc in self.get_piece_moveable_positions(r, c):
                        if self.board[tr][tc] != '--' and self.board[tr][tc][0] != color:
                            captures.append((r, c, tr, tc))
        return captures

    def get_all_valid_moves(self, is_white_turn, verbose=False):
        player_color = 'w' if is_white_turn else 'b'
        all_moves_list = [] # list element is tupe of format (start_row, start_col, end_row, end_col)

        for row_num, row in enumerate(self.board):
            for col_num, piece in enumerate(row):
                # eval. moves for one color only whichever having its turn at current
                # Also filters out the empty sqaures
                if piece[0] == player_color:
                    # list of tuples contaiing end_row and end_col (the available next positions)
                    available_positions_to_move = self.get_piece_moveable_positions(row_num, col_num)
                    for (end_row, end_col) in available_positions_to_move:
                        # check if the move left the king cheked
                        move_obj = self.make_move(row_num, col_num, end_row, end_col)
                        if not self.is_king_in_check(player_color):
                            all_moves_list.append((row_num,col_num,end_row,end_col))
                        self.undo_move(move_obj)

        if verbose: # for debuggging purpose only
            print(f"Total moves for {'White' if is_white_turn else 'Black'}: {len(all_moves_list)}")
        return all_moves_list
    

    # returns ordered moves with valuable captures as priority
    # this improves alpha beta pruning
    def get_all_valid_moves_as_ordered(self, all_moves_unordered):
        # key function to make order
        def move_score(move):
            move_val = 0
            sr,sc,er,ec = move
            moving_piece = self.board[sr][sc]
            captured_piece = self.board[er][ec]
            # ensure that lower piece captures the highest piece first
            if captured_piece != '--':
            # MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
                move_val += self.PIECE_VALUES[captured_piece[1]] * 10 - self.PIECE_VALUES[moving_piece[1]]
            else:
            # Prioritize promotions or center control later
                move_val += 0
            # pawn promotion
            if moving_piece[1] == 'P' and er in [0,7]:
                move_val += 5
            return move_val 
            
        return sorted(all_moves_unordered, key=move_score, reverse=True)


    # Centerlised function to call appropriate moves-generator function accord. to piece-type
    def get_piece_moveable_positions(self, row, col):
        piece_type = self.board[row][col][1]

        if piece_type == 'P':
            return self.generate_pawn_moves(row, col)
        elif piece_type == 'N':
            return self.generate_knight_moves(row, col)
        elif piece_type == 'B':
            return self.generate_bishop_moves(row, col)
        elif piece_type == 'R':
            return self.generate_rook_moves(row, col)
        elif piece_type == 'Q':
            return self.generate_queen_moves(row, col)
        elif piece_type == 'K':
            return self.generate_king_moves(row, col)
        else:
            raise Exception("Unknown Piece !")
    

    def generate_pawn_moves(self, row, col):
        
        if self.board[row][col][1] != 'P':
            raise Exception("Expected pawn at the given position.")
        
        available_moves = []
        direction = -1 if self.board[row][col][0] == 'w' else 1

        if 0 <= (row + direction) < 8 and self.board[row + direction][col] == '--':
            available_moves.append((row + direction, col))
            if (direction == -1 and row == 6) or (direction == 1 and row == 1):
                if 0 <= (row + 2 * direction) < 8 and self.board[row + 2 * direction][col] == '--':
                    available_moves.append((row + 2 * direction, col))

        if 0 <= col - 1 < 8 and self.board[row + direction][col - 1] != '--' and self.board[row + direction][col - 1][0] != self.board[row][col][0]:
            available_moves.append((row + direction, col - 1))

        if 0 <= col + 1 < 8 and self.board[row + direction][col + 1] != '--' and self.board[row + direction][col + 1][0] != self.board[row][col][0]:
            available_moves.append((row + direction, col + 1))

        return available_moves


    def generate_rook_moves(self, row, col):
        
        if self.board[row][col][1] != "R":
            raise Exception("Expected rook at the given position.")
        
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        return self.generate_sliding_moves(row, col, directions)


    def generate_knight_moves(self, row, col):
        
        if self.board[row][col][1] != 'N':
            raise Exception("Expected knight at the given position.")
        
        directions = [
            (2, 1), (2, -1),
            (1, 2), (1, -2),
            (-2, 1), (-2, -1),
            (-1, -2), (-1, 2)
        ]
        color = self.board[row][col][0]
        available_moves = []

        for r_direction, c_direction in directions:
            new_row, new_col = row + r_direction, col + c_direction
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board[new_row][new_col] == '--' or self.board[new_row][new_col][0] != color:
                    available_moves.append((new_row, new_col))

        return available_moves


    def generate_bishop_moves(self, row, col):
        
        if self.board[row][col][1] != 'B':
            raise Exception("Expected bishop at the given position.")
        
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self.generate_sliding_moves(row, col, directions)


    def generate_queen_moves(self, row, col):
        
        if self.board[row][col][1] != 'Q':
            raise Exception("Expected queen at the given position.")
        
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, -1), (0, 1), (-1, 0), (1, 0)]
        return self.generate_sliding_moves(row, col, directions)


    def generate_king_moves(self, row, col):
        
        if self.board[row][col][1] != 'K':
            raise Exception("Expected king at the given position.")
        
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        color = self.board[row][col][0]
        available_moves = []

        # append general moves
        for r_direction, c_direction in directions:
            new_row, new_col = row + r_direction, col + c_direction
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.board[new_row][new_col] == '--' or self.board[new_row][new_col][0] != color:
                    available_moves.append((new_row, new_col))

        # append castling moves too
        if self.castling_rights[color]['K'] == True: # KING SIDE
            if self.board[row][5] == "--" and self.board[row][6] == "--":
                available_moves.append((row, 6))
        if self.castling_rights[color]['Q'] == True: # QUEEN SIDE
            if self.board[row][1] == "--" and self.board[row][2] == "--" and self.board[row][3] == "--":
                available_moves.append((row, 2))

        return available_moves


    def generate_sliding_moves(self, row, col, directions):
        
        color = self.board[row][col][0]
        available_moves = []

        for r_direction, c_direction in directions:
            new_row, new_col = row, col
            while True:
                new_row += r_direction
                new_col += c_direction
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board[new_row][new_col] == '--':
                        available_moves.append((new_row, new_col))
                    else:
                        if self.board[new_row][new_col][0] != color:
                            available_moves.append((new_row, new_col))
                        break
                else:
                    break
        
        return available_moves


    # convert human friendly move-denotion to machine friendly
    def algebraic_to_index(self, move_str):
        # (e2e4) --> ((6,4), (4,4))
        start_row = 8 - int(move_str[1])
        start_col = ord(move_str[0]) - 97
        end_row = 8 - int(move_str[3])
        end_col = ord(move_str[2]) - 97

        return (start_row, start_col, end_row, end_col)


    # convert machine denotion to human denotion (int terms of chess move)
    def index_to_algebraic(self, start_row, start_col, end_row, end_col):
        # ((6,4), (4,4)) --> (e2e4)
        start_file = chr(start_col + 97)
        start_rank = str(8-start_row)
        end_file = chr(end_col + 97)
        end_rank = str(8-end_row)

        return (start_file+start_rank+end_file+end_rank)

    def is_king_in_check(self, color):
        king_row, king_col = self.king_positions[color]
        return self.is_square_attacked(king_row, king_col, by_white=(color == 'b'))

    
    def compute_zobrist_hash(self):
        hash_value = 0
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '--':
                    piece_char = piece[1].upper() if piece[0] == 'w' else piece[1].lower()
                    idx = self.PIECE_TO_INDEX[piece_char]
                    hash_value ^= self.ZOBRIST_TABLE[row][col][idx]
        return hash_value

    # check if the current square is under attack by any piece
    def is_square_attacked(self, row, col, by_white):
        enemy_color = 'w' if by_white else 'b'
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (1, 0), (0, -1), (1, 1), (0, 1)]  # All directions

        # Check for pawn attacks
        pawn_dir = -1 if by_white else 1
        for dc in [-1, 1]:
            r, c = row + pawn_dir, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] == enemy_color + 'P':
                    return True

        # Check for knight attacks
        knight_moves = [(-2, -1), (-1, -2), (-2, 1), (-1, 2), (1, -2), (2, -1), (2, 1), (1, 2)]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] == enemy_color + 'N':
                    return True

        # Check for sliding piece attacks (bishops, rooks, queens)
        sliding_dirs = {
            'B': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
            'R': [(-1, 0), (1, 0), (0, -1), (0, 1)],
            'Q': [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        }
        for piece, dirs in sliding_dirs.items():
            for dr, dc in dirs:
                r, c = row + dr, col + dc
                while 0 <= r < 8 and 0 <= c < 8:
                    square = self.board[r][c]
                    if square != '--':
                        if square[0] == enemy_color and square[1] in piece:
                            return True
                        break
                    r += dr
                    c += dc

        # Check for king attack
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] == enemy_color + 'K':
                    return True

        return False

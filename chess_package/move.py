import copy

class Move:
    def __init__(self, start_row, start_col, end_row, end_col, moved_piece, captured_piece, isCheck=False, isPromoted=False, isReallyCaptured=False, hasCastled=False, prevCastlingRight=None):
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.moved_piece = moved_piece
        self.captured_piece = captured_piece
        self.isCheck = isCheck
        self.isPromoted = isPromoted
        self.isReallyCaptured = isReallyCaptured
        self.hasCastled = hasCastled
        self.prevCastlingRight = copy.deepcopy(prevCastlingRight)

    def __str__(self):
        return f"{self.moved_piece} from ({self.start_row},{self.start_col}) to ({self.end_row},{self.end_col}) {', captured ' + self.captured_piece if self.isReallyCaptured else ''}"

from chess_package import *


# quick play
def play_game(depth):
    state = Chess_State()
    engine = Engine()

    white_to_move = True

    while True:
        state.print_board()

        if white_to_move:
            user_input = input("Enter your move (e.g., e2e4 or 'q' to quit): ")
            if user_input.lower() == 'q':
                break

            try:
                sr, sc, er, ec = state.algebraic_to_index(user_input)
                all_moves = state.get_all_valid_moves_as_ordered(state.get_all_valid_moves(white_to_move))
                if (sr, sc, er, ec) in all_moves:
                    move_obj = state.make_move(sr, sc, er, ec)
                else:
                    print("Invalid move. Try again.")
                    continue
            except Exception as e:
                print("Invalid format. Use e.g. e2e4.")
                continue

        else:
            print("AI is thinking...")
            best_move = engine.get_best_move(state, depth, is_white_move = False)
            if best_move is None:
                print("AI resigns. You win!")
                break
            state.make_move(best_move.start_row, best_move.start_col,
                      best_move.end_row, best_move.end_col)
            print(f"AI played:{best_move.moved_piece} {state.index_to_algebraic(best_move.start_row, best_move.start_col,
                      best_move.end_row, best_move.end_col)}")

        white_to_move = not white_to_move



def stats(depth):
    # Tests
    import time
    engine = Engine()
    state = Chess_State()

    start_time = time.perf_counter()
    move = engine.get_best_move(state, depth, True)
    end_time = time.perf_counter()

    print(f"\nbest move: {move.moved_piece}, {state.index_to_algebraic(move.start_row,move.start_col, move.end_row, move.end_col)}")

    print(f"depth:{depth}")
    print(f"search time {end_time-start_time}")
    print(f"branches:{engine.branch}\nprunings:{engine.pruned}\nposition-hit:{engine.hit}\nnodes:{engine.node_cnt}")



if __name__ == "__main__":
    depth = 2
    play_game(depth)
    # stats(depth)

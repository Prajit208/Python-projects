# A basic chess game: 2 player + Minimax AI
from tkinter import *

root = Tk()
root.title("Chess")

'''Variables declaration'''
#############
spacing = 80
rows = 8
cols = 8
padding = 30  # space for rank/file labels
cell = None
board = [[cell for _ in range(cols)] for _ in range(rows)]

# Black pieces
board[0][0] = ["Rook", "Black", False]
board[0][1] = ["Knight", "Black"]
board[0][2] = ["Bishop", "Black"]
board[0][3] = ["Queen", "Black"]
board[0][4] = ["King", "Black", False]
board[0][5] = ["Bishop", "Black"]
board[0][6] = ["Knight", "Black"]
board[0][7] = ["Rook", "Black", False]
for c in range(8):
    board[1][c] = ["Pawn", "Black"]

# White pieces
board[7][0] = ["Rook", "White", False]
board[7][1] = ["Knight", "White"]
board[7][2] = ["Bishop", "White"]
board[7][3] = ["Queen", "White"]
board[7][4] = ["King", "White", False]
board[7][5] = ["Bishop", "White"]
board[7][6] = ["Knight", "White"]
board[7][7] = ["Rook", "White", False]
for c in range(8):
    board[6][c] = ["Pawn", "White"]

symbols = {
    ("Pawn", "White"): "♙", ("Knight", "White"): "♘",
    ("Bishop", "White"): "♗", ("Rook", "White"): "♖",
    ("Queen", "White"): "♕", ("King", "White"): "♔",
    ("Pawn", "Black"): "♟", ("Knight", "Black"): "♞",
    ("Bishop", "Black"): "♝", ("Rook", "Black"): "♜",
    ("Queen", "Black"): "♛", ("King", "Black"): "♚",
}

source_cell = None
destination_cell = None
hovered_cell = None
turn = "White"
ai_has_moved = False
move_log = []  # stores move strings
##############

# Canvas is 640+padding wide, 640+padding tall
canvas = Canvas(root, width=640 + padding, height=640 + padding,
                bg="#2b2b2b", highlightthickness=0)
canvas.pack(side=LEFT)

# Move tracker panel on the right
frame = Frame(root, bg="#1e1e1e", width=200)
frame.pack(side=RIGHT, fill=Y)

Label(frame, text="Move History", bg="#1e1e1e", fg="white",
      font=("Courier", 13, "bold"), pady=8).pack()

move_listbox = Listbox(frame, bg="#1e1e1e", fg="#d4d4d4",
                       font=("Courier", 10), selectbackground="#3c3c3c",
                       borderwidth=0, highlightthickness=0, width=22)
move_listbox.pack(fill=BOTH, expand=True, padx=6, pady=4)

scrollbar = Scrollbar(frame, command=move_listbox.yview, bg="#3c3c3c")
scrollbar.pack(side=RIGHT, fill=Y)
move_listbox.config(yscrollcommand=scrollbar.set)

turn_label = Label(frame, text="Turn: White", bg="#1e1e1e", fg="#f0d9b5",
                   font=("Courier", 11, "bold"), pady=6)
turn_label.pack()


def col_to_file(col):
    return chr(ord('a') + col)


def row_to_rank(row):
    return str(8 - row)


def log_move(piece_name, color, src_row, src_col, dst_row, dst_col):
    src = col_to_file(src_col) + row_to_rank(src_row)
    dst = col_to_file(dst_col) + row_to_rank(dst_row)
    prefix = "W" if color == "White" else "B"
    entry = f"{prefix}  {piece_name[:2]} {src}→{dst}"
    move_log.append(entry)
    move_listbox.insert(END, entry)
    move_listbox.yview(END)
    turn_label.config(text=f"Turn: {'Black' if color == 'White' else 'White'}")


def board_render():
    # Draw squares
    for row in range(8):
        for col in range(8):
            x1 = col * spacing + padding
            y1 = row * spacing
            x2 = x1 + spacing
            y2 = y1 + spacing
            color = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
            if [row, col] == hovered_cell:
                canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=5)

    # File labels (a-h) along the bottom
    files = "abcdefgh"
    for col in range(8):
        x = col * spacing + padding + spacing // 2
        y = 640 + padding // 2
        canvas.create_text(x, y, text=files[col], fill="#d4d4d4",
                           font=("Courier", 11, "bold"))

    # Rank labels (8-1) along the left
    for row in range(8):
        x = padding // 2
        y = row * spacing + spacing // 2
        canvas.create_text(x, y, text=str(8 - row), fill="#d4d4d4",
                           font=("Courier", 11, "bold"))


def render_piece():
    for row in range(rows):
        for col in range(cols):
            piece = board[row][col]
            if piece is not None:
                symbol = symbols[(piece[0], piece[1])]
                x = col * spacing + padding + spacing // 2
                y = row * spacing + spacing // 2
                canvas.create_text(x, y, text=symbol, font=("Arial", 36))

                if is_in_check(board[row][col][1]):
                    if board[row][col][0] == "King":
                        x1 = col * spacing + padding
                        y1 = row * spacing
                        canvas.create_rectangle(x1, y1, x1 + spacing, y1 + spacing,
                                                outline="red", width=5)


def move_piece(event):
    global destination_cell, source_cell, turn, ai_has_moved
    col = (event.x - padding) // spacing
    row = event.y // spacing

    if col < 0 or col >= 8 or row < 0 or row >= 8:
        return

    if source_cell is None and board[row][col] is not None and board[row][col][1] != turn:
        return

    if source_cell is None:
        if board[row][col] is not None:
            source_cell = [row, col]
    else:
        x, y = source_cell
        if valid_move(x, y, row, col, execute=True):
            prev_piece = board[row][col]
            piece_name = board[x][y][0]
            piece_color = board[x][y][1]
            board[row][col] = board[x][y]
            board[x][y] = None
            if is_in_check(board[row][col][1]):
                board[x][y] = board[row][col]
                board[row][col] = prev_piece
            else:
                if board[row][col][0] in ["King", "Rook"]:
                    board[row][col][2] = True
                if board[row][col][0] == "Pawn":
                    if row == 0:
                        board[row][col] = ["Queen", "White"]
                    if row == 7:
                        board[row][col] = ["Queen", "Black"]
                log_move(piece_name, piece_color, x, y, row, col)
                turn = "Black" if piece_color == "White" else "White"
                ai_has_moved = False
        source_cell = None


def valid_move(src_row, src_col, dst_row, dst_col, checking=False, execute=False):
    valid = False
    if board[dst_row][dst_col] is not None:
        if board[dst_row][dst_col][1] == board[src_row][src_col][1]:
            return False
    if board[src_row][src_col][0] == "Knight":
        knight_jump = [(-2, -1), (-2, 1), (-1, -2), (1, -2),
                       (2, 1), (2, -1), (1, 2), (-1, 2)]
        for dir_row, dir_col in knight_jump:
            new_row, new_col = src_row + dir_row, src_col + dir_col
            if 0 <= new_row < rows and 0 <= new_col < cols:
                if dst_row == new_row and dst_col == new_col:
                    valid = True

    elif board[src_row][src_col][0] == "Pawn":
        if src_row == 6 and board[src_row][src_col][1] == "White":
            if checking:
                if (dst_col == src_col - 1 and dst_row == src_row - 1) or \
                   (dst_col == src_col + 1 and dst_row == src_row - 1):
                    valid = True
            elif dst_col == src_col and (dst_row == src_row - 2 or dst_row == src_row - 1):
                if board[src_row - 1][dst_col] is not None or board[dst_row][dst_col] is not None:
                    return False
                valid = True
            elif (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "Black" and
                  dst_col == src_col - 1 and dst_row == src_row - 1) or \
                 (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "Black" and
                  dst_col == src_col + 1 and dst_row == src_row - 1):
                valid = True
        elif src_row == 1 and board[src_row][src_col][1] == "Black":
            if checking:
                if (dst_col == src_col - 1 and dst_row == src_row + 1) or \
                   (dst_col == src_col + 1 and dst_row == src_row + 1):
                    valid = True
            elif dst_col == src_col and (dst_row == src_row + 2 or dst_row == src_row + 1):
                if board[src_row + 1][dst_col] is not None or board[dst_row][dst_col] is not None:
                    return False
                valid = True
            elif (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "White" and
                  dst_col == src_col - 1 and dst_row == src_row + 1) or \
                 (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "White" and
                  dst_col == src_col + 1 and dst_row == src_row + 1):
                valid = True
        else:
            if board[src_row][src_col][1] == "White":
                if dst_col == src_col and dst_row == src_row - 1:
                    if board[dst_row][dst_col] is not None:
                        return False
                    valid = True
                if checking:
                    if (dst_col == src_col - 1 and dst_row == src_row - 1) or \
                       (dst_col == src_col + 1 and dst_row == src_row - 1):
                        valid = True
                elif (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "Black" and
                      dst_col == src_col - 1 and dst_row == src_row - 1) or \
                     (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "Black" and
                      dst_col == src_col + 1 and dst_row == src_row - 1):
                    valid = True
            elif board[src_row][src_col][1] == "Black":
                if dst_col == src_col and dst_row == src_row + 1:
                    if board[dst_row][dst_col] is not None:
                        return False
                    valid = True
                if checking:
                    if (dst_col == src_col - 1 and dst_row == src_row + 1) or \
                       (dst_col == src_col + 1 and dst_row == src_row + 1):
                        valid = True
                elif (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "White" and
                      dst_col == src_col - 1 and dst_row == src_row + 1) or \
                     (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "White" and
                      dst_col == src_col + 1 and dst_row == src_row + 1):
                    valid = True

    elif board[src_row][src_col][0] == "Rook":
        if dst_row == src_row:
            step = 1 if dst_col > src_col else -1
            for c in range(src_col + step, dst_col, step):
                if board[src_row][c] is not None:
                    return False
            valid = True
        elif dst_col == src_col:
            step = 1 if dst_row > src_row else -1
            for r in range(src_row + step, dst_row, step):
                if board[r][src_col] is not None:
                    return False
            valid = True

    elif board[src_row][src_col][0] == "Bishop":
        row_step = 1 if dst_row > src_row else -1
        col_step = 1 if dst_col > src_col else -1
        if abs(src_row - dst_row) == abs(src_col - dst_col):
            for i in range(1, abs(dst_row - src_row)):
                if board[src_row + row_step * i][src_col + col_step * i] is not None:
                    return False
            valid = True

    elif board[src_row][src_col][0] == "Queen":
        if dst_row == src_row:
            step = 1 if dst_col > src_col else -1
            for c in range(src_col + step, dst_col, step):
                if board[src_row][c] is not None:
                    return False
            valid = True
        elif dst_col == src_col:
            step = 1 if dst_row > src_row else -1
            for r in range(src_row + step, dst_row, step):
                if board[r][src_col] is not None:
                    return False
            valid = True
        elif abs(src_row - dst_row) == abs(src_col - dst_col):
            row_step = 1 if dst_row > src_row else -1
            col_step = 1 if dst_col > src_col else -1
            for i in range(1, abs(dst_row - src_row)):
                if board[src_row + row_step * i][src_col + col_step * i] is not None:
                    return False
            valid = True

    elif board[src_row][src_col][0] == "King":
        king_direction = [(1, 0), (-1, 0), (1, 1), (-1, -1),
                          (0, 1), (0, -1), (1, -1), (-1, 1)]
        for dir_row, dir_col in king_direction:
            new_row, new_col = src_row + dir_row, src_col + dir_col
            if dst_row == new_row and dst_col == new_col:
                valid = True
        if board[src_row][src_col][2] == False:
            if src_col - 4 >= 0 and board[src_row][src_col - 4] is not None and \
               board[src_row][src_col - 4][0] == "Rook":
                if board[src_row][src_col - 4][2] == False:
                    if board[src_row][src_col - 3] is None and \
                       board[src_row][src_col - 2] is None and \
                       board[src_row][src_col - 1] is None:
                        if dst_row == src_row and dst_col == src_col - 2:
                            if execute:
                                board[src_row][src_col - 1] = board[src_row][src_col - 4]
                                board[src_row][src_col - 4] = None
                            valid = True
            if src_col + 3 <= 7 and board[src_row][src_col + 3] is not None and \
               board[src_row][src_col + 3][0] == "Rook":
                if board[src_row][src_col + 3][2] == False:
                    if board[src_row][src_col + 1] is None and \
                       board[src_row][src_col + 2] is None:
                        if dst_row == src_row and dst_col == src_col + 2:
                            if execute:
                                board[src_row][src_col + 1] = board[src_row][src_col + 3]
                                board[src_row][src_col + 3] = None
                            valid = True
    return valid


def is_in_check(color):
    enemy_color = "Black" if color == "White" else "White"
    king_row, king_col = 0, 0
    for row in range(rows):
        for col in range(cols):
            if board[row][col] is not None and board[row][col][0] == "King" and \
               board[row][col][1] == color:
                king_row, king_col = row, col
    for row in range(rows):
        for col in range(cols):
            if board[row][col] is not None and board[row][col][1] == enemy_color:
                if valid_move(row, col, king_row, king_col, checking=True):
                    return True
    return False


def checkmate(color):
    if not is_in_check(color):
        return False
    for row in range(rows):
        for col in range(cols):
            for dst_row in range(rows):
                for dst_col in range(cols):
                    if board[row][col] is not None and board[row][col][1] == color:
                        if valid_move(row, col, dst_row, dst_col):
                            prev = board[dst_row][dst_col]
                            board[dst_row][dst_col] = board[row][col]
                            board[row][col] = None
                            still_in_check = is_in_check(color)
                            board[row][col] = board[dst_row][dst_col]
                            board[dst_row][dst_col] = prev
                            if not still_in_check:
                                return False
    return True


def hover(event):
    global hovered_cell
    col = (event.x - padding) // spacing
    row = event.y // spacing
    if 0 <= col < 8 and 0 <= row < 8:
        hovered_cell = [row, col]
    else:
        hovered_cell = None


def evaluate_board():
    piece_value = {"Pawn": 1, "Knight": 3, "Bishop": 3,
                   "Rook": 5, "Queen": 9, "King": 1000}
    score = 0
    for row in range(rows):
        for col in range(cols):
            if board[row][col] is not None:
                val = piece_value[board[row][col][0]]
                if board[row][col][1] == "White":
                    score += val
                else:
                    score -= val
    return score


def minimax(depth, isMaximizing, alpha, beta):
    if checkmate("White"):
        return -10000
    if checkmate("Black"):
        return 10000
    if depth == 0:
        return evaluate_board()

    if isMaximizing:
        best_score = -float('inf')
        for row in range(rows):
            for col in range(cols):
                if board[row][col] is not None and board[row][col][1] == "White":
                    for dst_row in range(rows):
                        for dst_col in range(cols):
                            if board[row][col][0] == "King" and abs(dst_col - col) == 2:
                                continue
                            if valid_move(row, col, dst_row, dst_col):
                                prev = board[dst_row][dst_col]
                                board[dst_row][dst_col] = board[row][col]
                                board[row][col] = None
                                if is_in_check("White"):
                                    board[row][col] = board[dst_row][dst_col]
                                    board[dst_row][dst_col] = prev
                                    continue
                                result = minimax(depth - 1, False, alpha, beta)
                                board[row][col] = board[dst_row][dst_col]
                                board[dst_row][dst_col] = prev
                                best_score = max(best_score, result)
                                alpha = max(alpha, best_score)
                                if beta <= alpha:
                                    return best_score
        return best_score
    else:
        best_score = float('inf')
        for row in range(rows):
            for col in range(cols):
                if board[row][col] is not None and board[row][col][1] == "Black":
                    for dst_row in range(rows):
                        for dst_col in range(cols):
                            if board[row][col][0] == "King" and abs(dst_col - col) == 2:
                                continue
                            if valid_move(row, col, dst_row, dst_col):
                                prev = board[dst_row][dst_col]
                                board[dst_row][dst_col] = board[row][col]
                                board[row][col] = None
                                if is_in_check("Black"):
                                    board[row][col] = board[dst_row][dst_col]
                                    board[dst_row][dst_col] = prev
                                    continue
                                result = minimax(depth - 1, True, alpha, beta)
                                board[row][col] = board[dst_row][dst_col]
                                board[dst_row][dst_col] = prev
                                best_score = min(best_score, result)
                                beta = min(beta, best_score)
                                if beta <= alpha:
                                    return best_score
        return best_score


def get_best_move(depth):
    best_score = float('inf')
    best_move = None
    alpha = -float('inf')
    beta = float('inf')

    for row in range(rows):
        for col in range(cols):
            if board[row][col] is not None and board[row][col][1] == "Black":
                for dst_row in range(rows):
                    for dst_col in range(cols):
                        if board[row][col][0] == "King" and abs(dst_col - col) == 2:
                            continue
                        if valid_move(row, col, dst_row, dst_col):
                            prev = board[dst_row][dst_col]
                            board[dst_row][dst_col] = board[row][col]
                            board[row][col] = None
                            if is_in_check("Black"):
                                board[row][col] = board[dst_row][dst_col]
                                board[dst_row][dst_col] = prev
                                continue
                            result = minimax(depth - 1, True, alpha, beta)
                            board[row][col] = board[dst_row][dst_col]
                            board[dst_row][dst_col] = prev
                            if result < best_score:
                                best_score = result
                                best_move = [row, col, dst_row, dst_col]
                            beta = min(beta, best_score)
    return best_move


def game_run():
    global turn, ai_has_moved

    canvas.delete("all")
    board_render()
    render_piece()

    if turn == "Black":
        if not ai_has_moved:
            move = get_best_move(3)
            if move is None:
                return
            a, b, c, d = move
            piece_name = board[a][b][0]
            piece_color = board[a][b][1]
            prev_piece = board[c][d]
            board[c][d] = board[a][b]
            board[a][b] = None
            if is_in_check(board[c][d][1]):
                board[a][b] = board[c][d]
                board[c][d] = prev_piece
            else:
                if board[c][d][0] in ["King", "Rook"]:
                    board[c][d][2] = True
                if board[c][d][0] == "Pawn" and c == 7:
                    board[c][d] = ["Queen", "Black"]
                if board[c][d][0] == "King":
                    if d - b == 2:
                        board[c][d + 1] = board[c][d + 3]
                        board[c][d + 3] = None
                        board[c][d + 1][2] = True
                    elif b - d == 2:
                        board[c][d - 1] = board[c][d - 4]
                        board[c][d - 4] = None
                        board[c][d - 1][2] = True
                log_move(piece_name, piece_color, a, b, c, d)
                turn = "White"
                ai_has_moved = True

    if checkmate(turn):
        canvas.create_text(320 + padding // 2, 320,
                           text=f"{turn} is in checkmate!",
                           fill="white", font=("Arial", 24))
        return

    root.after(20, game_run)


canvas.bind("<Button-1>", move_piece)
canvas.bind("<Motion>", hover)
root.after(20, game_run)
root.mainloop()
# A basic chess game: 2 player
from tkinter import *

root=Tk() 
root.title("Chess")

'''Variables declaration'''
#############
spacing=80
rows=8
cols=8
cell=None
board=[[cell for _ in range(cols)] for _ in range(rows)]
# Black piece
board[0][0]=["Rook","Black",False]
board[0][1]=["Knight","Black"]
board[0][2]=["Bishop","Black"]
board[0][3]=["Queen","Black"]
board[0][4]=["King","Black",False]
board[0][5]=["Bishop","Black"]
board[0][6]=["Knight","Black"]
board[0][7]=["Rook","Black",False]

board[1][0]=["Pawn","Black"]
board[1][1]=["Pawn","Black"]
board[1][2]=["Pawn","Black"]
board[1][3]=["Pawn","Black"]
board[1][4]=["Pawn","Black"]
board[1][5]=["Pawn","Black"]
board[1][6]=["Pawn","Black"]
board[1][7]=["Pawn","Black"]

# White piece
board[7][0]=["Rook","White",False]
board[7][1]=["Knight","White"]
board[7][2]=["Bishop","White"]
board[7][3]=["Queen","White"]
board[7][4]=["King","White",False]
board[7][5]=["Bishop","White"]
board[7][6]=["Knight","White"]
board[7][7]=["Rook","White",False]

board[6][0]=["Pawn","White"]
board[6][1]=["Pawn","White"]
board[6][2]=["Pawn","White"]
board[6][3]=["Pawn","White"]
board[6][4]=["Pawn","White"]
board[6][5]=["Pawn","White"]
board[6][6]=["Pawn","White"]
board[6][7]=["Pawn","White"]

symbols = {
    ("Pawn", "White"): "♙",
    ("Knight", "White"): "♘",
    ("Bishop", "White"): "♗",
    ("Rook", "White"): "♖",
    ("Queen", "White"): "♕",
    ("King", "White"): "♔",
    ("Pawn", "Black"): "♟",
    ("Knight", "Black"): "♞",
    ("Bishop", "Black"): "♝",
    ("Rook", "Black"): "♜",
    ("Queen", "Black"): "♛",
    ("King", "Black"): "♚",
}

source_cell=None
destination_cell=None
hovered_cell=None
turn="White"
ai_has_moved=False
##############

canvas= Canvas(root, width=640, height=640, bg="black",highlightthickness=2,highlightbackground="black")
def board_render():
    for row in range(8):
        for col in range(8):
            x1 = col * spacing
            y1 = row * spacing
            x2 = x1 + spacing
            y2 = y1 + spacing
        # Alternate colors: white on even (row+col), black on odd
            color = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
            if([row,col]==hovered_cell):
                canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=5)                       

def render_piece():
    for row in range(rows):
        for col in range(cols):
            piece = board[row][col]
            if piece is not None:
                symbol = symbols[(piece[0], piece[1])]
                x1 = col * spacing
                y1 = row * spacing
                canvas.create_text(x1+40, y1+40, text=symbol, font=("Arial", 36))
                
                if is_in_check(board[row][col][1]):
                    if(board[row][col][0]=="King"):
                        x=col * spacing
                        y= row * spacing
                        canvas.create_rectangle(x,y,x+spacing,y+spacing,outline="red",width=5)

def draw_labels():
    files = ['a','b','c','d','e','f','g','h']
    
    # files (bottom)
    for col in range(cols):
        x = col * spacing + spacing//2
        canvas.create_text(x, 640-10, text=files[col], font=("Arial", 10))

    # ranks (left)
    for row in range(rows):
        y = row * spacing + spacing//2
        canvas.create_text(10, y, text=str(8-row), font=("Arial", 10))
def move_piece(event):
    global destination_cell, source_cell,turn,ai_has_moved
    col = event.x // spacing
    row = event.y // spacing
    
    if source_cell is None and board[row][col] is not None and board[row][col][1]!=turn: # checks the turn if the selefcted cell is not the same as turncolor it just exits fromt he function
        return
    
    if(source_cell is None):
        if(board[row][col] is not None):
            source_cell=[row,col]
        
    else:
        x,y=source_cell# x,y are source, rowcolare destination 
        if valid_move(x,y,row,col,execute=True):
            
            prev_piece=board[row][col] # saves original position before moving
            board[row][col]=board[x][y] # moves
            
            board[x][y]=None
            if is_in_check(board[row][col][1]):
                board[x][y]=board[row][col] # put piece back 
                board[row][col]=prev_piece # restore destination

            else:
                if(board[row][col][0]=="King" or board[row][col][0]=="Rook"):
                    board[row][col][2]=True
                if(board[row][col][0]=="Pawn"):
                    if row==0:
                        board[row][col]=["Queen","White"]
                    if row==7:
                        board[row][col]=["Queen","Black"]        
                turn="Black" if board[row][col][1]=="White" else "White" 
                
                ai_has_moved = False# undo/ invalidate/ error throw
        source_cell=None
       
def valid_move(src_row,src_col,dst_row,dst_col,checking=False,execute=False):
    valid = False
    if board[dst_row][dst_col] is not None: # deny capture own piece
        if board[dst_row][dst_col][1] == board[src_row][src_col][1]:
            return False 
    if(board[src_row][src_col][0]=="Knight"):# vertical=row horizontal=col order=row,col, right,down= positive, up,left=negative
        knight_jump=[(-2,-1),(-2,1),(-1,-2),(1,-2),(2,1),(2,-1),(1,2),(-1,2)] # up.left up.right left.up left.down right.up right.down down.right down.left
        for dir_row,dir_col in knight_jump:
            new_row, new_col= src_row+dir_row, src_col+dir_col
            if 0<=new_row<rows and 0<=new_col<cols: # boundary check
                  if(dst_row==new_row and dst_col==new_col):
                      valid= True 
    # defines pawns movement
    elif(board[src_row][src_col][0]=="Pawn"): 
   
        if(src_row==6 and board[src_row][src_col][1]=="White"):# white's first move check
            if checking:# check to king checking
                    if(dst_col==src_col-1 and dst_row==src_row-1) or (dst_col==src_col+1 and dst_row==src_row-1):
                        valid= True
            elif(dst_col==src_col and (dst_row==src_row-2 or dst_row==src_row-1)):# one cell or 2 cell move check
                
                if board[src_row-1][dst_col] is not None or board[dst_row][dst_col] is not None:# jump and occupied cell check
                    return False
                valid=True
            elif (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "Black" and dst_col==src_col-1 and dst_row==src_row-1) or \
                (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "Black" and dst_col==src_col+1 and dst_row==src_row-1):
                
                valid= True   
        elif(src_row==1 and board[src_row][src_col][1]=="Black"):
            if checking:
                    if(dst_col==src_col-1 and dst_row==src_row+1) or (dst_col==src_col+1 and dst_row==src_row+1):
                        valid= True
            elif(dst_col==src_col and (dst_row==src_row+2 or dst_row==src_row+1)):
                
                if board[src_row+1][dst_col] is not None or board[dst_row][dst_col] is not None:
                    return False
                valid=True
            elif (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "White" and dst_col==src_col-1 and dst_row==src_row+1) or \
                (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "White" and dst_col==src_col+1 and dst_row==src_row+1):
                valid= True    
                    
        else:
            if(board[src_row][src_col][1]=="White"):
                if(dst_col==src_col and dst_row==src_row-1):
                    if board[dst_row][dst_col] is not None:
                        return False
                    valid= True 
                    
                if checking:
                    if(dst_col==src_col-1 and dst_row==src_row-1) or (dst_col==src_col+1 and dst_row==src_row-1):
                        valid= True
                    
                elif (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "Black" and dst_col==src_col-1 and dst_row==src_row-1) or \
                (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "Black" and dst_col==src_col+1 and dst_row==src_row-1):
                
                    valid= True
                    
            elif(board[src_row][src_col][1]=="Black"):
                if(dst_col==src_col and dst_row==src_row+1):
                    if board[dst_row][dst_col] is not None:
                        return False
                    valid= True 
                if checking:
                    if(dst_col==src_col-1 and dst_row==src_row+1) or (dst_col==src_col+1 and dst_row==src_row+1):
                        valid= True
                elif (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "White" and dst_col==src_col-1 and dst_row==src_row+1) or \
                (board[dst_row][dst_col] is not None and board[dst_row][dst_col][1] == "White" and dst_col==src_col+1 and dst_row==src_row+1):
                
                    valid= True 
                     
    
    # Rook movement defination            
    elif(board[src_row][src_col][0]=="Rook"):
        if dst_row==src_row:# Moves horizontal
            step=1 if dst_col>src_col else -1
            for col in range(src_col+step,dst_col,step):
                if board[src_row][col] is not None:
                    return False
            valid= True    
        elif dst_col==src_col: # Moves Vertical                
            step=1 if dst_row>src_row else -1  
            for row in range(src_row+step,dst_row,step):
                if board[row][src_col] is not None:
                    return False
            valid= True       
                
    elif(board[src_row][src_col][0]=="Bishop"):
        row_step = 1 if dst_row > src_row else -1
        col_step = 1 if dst_col > src_col else -1
        if(abs(src_row-dst_row)==abs(src_col-dst_col)):           
            
            for i in range(1,abs(dst_row-src_row)):
                
                if board[src_row +row_step* i][src_col+col_step*i] is not None:
                    return False
            valid= True 
    elif(board[src_row][src_col][0]=="Queen"): # just combine Rook and bishop logic
        
        if dst_row==src_row:# Moves horizontal
            step=1 if dst_col>src_col else -1
            for col in range(src_col+step,dst_col,step):
                if board[src_row][col] is not None:
                    return False
            valid= True    
        elif dst_col==src_col: # Moves Vertical                
            step=1 if dst_row>src_row else -1  
            for row in range(src_row+step,dst_row,step):
                if board[row][src_col] is not None:
                    return False
            valid= True 
        
        elif(abs(src_row-dst_row)==abs(src_col-dst_col)):
            row_step = 1 if dst_row > src_row else -1
            col_step = 1 if dst_col > src_col else -1           
            for i in range(1,abs(dst_row-src_row)):
                
                if board[src_row +row_step* i][src_col+col_step*i] is not None:
                    return False
            valid= True     
    
    # King's Movement defination
    elif(board[src_row][src_col][0]=="King"):
        king_direction=[(1,0),(-1,0),(1,1),(-1,-1),(0,1),(0,-1),(1,-1),(-1,1)]  
        for dir_row,dir_col in king_direction:
            new_row, new_col= src_row+dir_row, src_col+dir_col
            if(dst_row==new_row and dst_col==new_col):
                    valid= True
        if(board[src_row][src_col][2]==False):
            if src_col-4 >= 0 and board[src_row][src_col-4] is not None and board[src_row][src_col-4][0]=="Rook":
                if(board[src_row][src_col-4][2]==False):
                    if(board[src_row][src_col-3] is None and board[src_row][src_col-2] is None and board[src_row][src_col-1] is None):
                        if dst_row==src_row and dst_col==src_col-2:
                            if execute:
                                board[src_row][src_col-1] = board[src_row][src_col-4]
                                board[src_row][src_col-4] = None
                            valid=True 
            if src_col+3 <= 7 and board[src_row][src_col+3] is not None and board[src_row][src_col+3][0]=="Rook":
                if(board[src_row][src_col+3][2]==False):
                    if(board[src_row][src_col+1] is None and board[src_row][src_col+2] is None):
                        if dst_row==src_row and dst_col==src_col+2:
                            if execute:
                                board[src_row][src_col+1] = board[src_row][src_col+3]
                                board[src_row][src_col+3] = None
                            valid=True   
    return valid

def is_in_check(color):
    enemy_color = "Black" if color == "White" else "White"
    for row in range(rows):
        for col in range(cols):
            if board[row][col] is not None and board[row][col][0]=="King" and board[row][col][1]==color:
                king_row,king_col=row,col
    for row in range(rows):
        for col in range(cols):
            if(board[row][col] is not None and board[row][col][1]==enemy_color):
                if(valid_move(row,col,king_row,king_col,checking=True)):
                    
                    return True            
    
    return False
def checkmate(color):
    if is_in_check(color)==False:
        return False 
    # loop through every piece of color
    for row in range(rows):
        for col in range(cols):
           for dst_row in range(rows):
               for dst_col in range(cols):
                    if board[row][col] is not None and board[row][col][1]==color:
                        if valid_move(row,col,dst_row,dst_col,checking=False):
                            #simulate every option that can get you out of check, if not out of check , undo that   
                            prev= board[dst_row][dst_col]   # stores the item in destination cell incase of undo
                            board[dst_row][dst_col]=board[row][col] # copies whatever item is in source to destination
                            board[row][col]  = None # empties the source cell since piece moved
                            still_in_check= is_in_check(color) # new variable that find if the simulated movement got king out of check
                            #undo what we did , since its just simulation and not a player move
                            board[row][col]=board[dst_row][dst_col]
                            board[dst_row][dst_col]=prev
                            if still_in_check==False: # if simulation found a escape, checkmate has not happened 
                                return False # so return checkmeate false
    return True
canvas.pack()
def hover(event):
    global hovered_cell
    col = event.x // spacing
    row = event.y // spacing
    hovered_cell=[row,col]

def evaluate_board():
    piece_value={
        "Pawn": 1,
        "Knight":3,
        "Bishop": 3,
        "Rook":5,
        "Queen": 9,
        "King":1000
    }
    score=0
    for row in range(rows):
        for col in range(cols):
            if(board[row][col] is not None ):
                if(board[row][col][1]=="White"):
                    score=score + piece_value[board[row][col][0]]
                if(board[row][col][1]=="Black"):
                    score=score - piece_value[board[row][col][0]]
    return score                
                             
def minimax(depth, isMaximizing,alpha,beta):
    if checkmate("White"):
        return -10000
    if checkmate("Black"):
        return 10000

    if depth == 0:
        return evaluate_board()

    if isMaximizing:  # White
        best_score = -float('inf')

        for row in range(rows):
            for col in range(cols):
                if board[row][col] is not None and board[row][col][1] == "White":

                    for dst_row in range(rows):
                        for dst_col in range(cols):

                            # skip castling in minimax
                            if board[row][col][0] == "King" and abs(dst_col - col) == 2:
                                continue

                            if valid_move(row, col, dst_row, dst_col):
                                prev = board[dst_row][dst_col]
                                board[dst_row][dst_col] = board[row][col]
                                board[row][col] = None

                                #  illegal move check
                                if is_in_check("White"):
                                    board[row][col] = board[dst_row][dst_col]
                                    board[dst_row][dst_col] = prev
                                    continue

                                result = minimax(depth - 1, False,alpha,beta)

                                # undo
                                board[row][col] = board[dst_row][dst_col]
                                board[dst_row][dst_col] = prev

                                best_score = max(best_score, result)
                                alpha=max(alpha,best_score)
                                if beta<=alpha:
                                    return best_score
        return best_score

    else:  # Black
        best_score = float('inf')

        for row in range(rows):
            for col in range(cols):
                if board[row][col] is not None and board[row][col][1] == "Black":

                    for dst_row in range(rows):
                        for dst_col in range(cols):

                            # skip castling in minimax
                            if board[row][col][0] == "King" and abs(dst_col - col) == 2:
                                continue

                            if valid_move(row, col, dst_row, dst_col):
                                prev = board[dst_row][dst_col]
                                board[dst_row][dst_col] = board[row][col]
                                board[row][col] = None

                                # illegal move check
                                if is_in_check("Black"):
                                    board[row][col] = board[dst_row][dst_col]
                                    board[dst_row][dst_col] = prev
                                    continue

                                result = minimax(depth - 1, True,alpha,beta)

                                # undo
                                board[row][col] = board[dst_row][dst_col]
                                board[dst_row][dst_col] = prev

                                best_score = min(best_score, result)
                                beta=min(beta,best_score)
                                if beta<=alpha:
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

                        # skip castling in minimax
                        if board[row][col][0] == "King" and abs(dst_col - col) == 2:
                            continue

                        if valid_move(row, col, dst_row, dst_col):
                            prev = board[dst_row][dst_col]
                            board[dst_row][dst_col] = board[row][col]
                            board[row][col] = None

                            #  illegal move check
                            if is_in_check("Black"):
                                board[row][col] = board[dst_row][dst_col]
                                board[dst_row][dst_col] = prev
                                continue

                            result = minimax(depth - 1, True,-float('inf'), float('inf'))

                            # undo
                            board[row][col] = board[dst_row][dst_col]
                            board[dst_row][dst_col] = prev

                            if result < best_score:
                                best_score = result
                                best_move = [row, col, dst_row, dst_col]

    return best_move                     
def game_run():
    global turn, ai_has_moved

    canvas.delete("all")
    
    board_render()
    draw_labels()
    render_piece()

    if turn == "Black":
        if not ai_has_moved:
            move = get_best_move(4)

            if move is None:
                return

            a, b, c, d = move

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

                # castling
                if board[c][d][0] == "King":
                    if d - b == 2:
                        board[c][d+1] = board[c][d+3]
                        board[c][d+3] = None
                        board[c][d+1][2] = True
                    elif b - d == 2:
                        board[c][d-1] = board[c][d-4]
                        board[c][d-4] = None
                        board[c][d-1][2] = True

                turn = "White"
                ai_has_moved = True

    if checkmate(turn):
        canvas.create_text(320, 320, text=f"{turn} is in checkmate!", fill="white", font=("Arial", 24))
        return

    root.after(20, game_run)

root.bind("<Button-1>", move_piece)
canvas.bind("<Motion>", hover)
root.after(20,game_run)
root.mainloop()
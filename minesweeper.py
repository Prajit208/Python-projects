# A classic game of minesweeper

from tkinter import *
import random
spacing=40
rows=5
cols=15
cell={
    "mine": False,
    "revealed": False,
    "flagged": False,
    "number": 0
}
grid_content=[[cell.copy() for _ in range(cols)] for _ in range(rows)]
mine_count=5
game_win=False
def fills_mines():
    mine_position=random.sample(range(rows* cols),mine_count)
    for pos in mine_position:
        row,col= divmod(pos,cols)
        grid_content[row][col]["mine"]=True
    # print(grid_content)  
root =Tk()
canvas= Canvas(root,width=600,height=200, bg="gray")
canvas.pack()
def calc_neighbor():
    # For each cell, check its 8 neighbors using row/col offsets (e.g. right = row+0, col+1)
    # For each direction, if the neighbor cell has mine=True, increment count by 1
    # Store final count in the cell's "number" key
    
    direction=[(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]
    #    right, left, down, up, down.right, up.right, down.left, up.left 
    for row in range(rows):
        for col in range(cols): # loops through every cell
            for dir_row, dir_col in direction: # loops through each direction
                new_row, new_col= row+dir_row, col+dir_col
                if 0<=new_row<rows and 0<=new_col<cols: # checks boundary
                    if(grid_content[new_row][new_col]["mine"]==True): # Checks if neighbor cell contain mines
                        grid_content[row][col]["number"]+=1 # adds number if number detected
    

def render_grid():
    for x in range(0,600,spacing):
        canvas.create_line(x,0,x,200, fill="black")
    for y in range(0,200,spacing):
        canvas.create_line(0,y,600,y,fill="black")    
    for row in range(rows):
        for col in range(cols):
            if(grid_content[row][col]["flagged"]==True and grid_content[row][col]["revealed"]==False ):
                x1=col * 40
                y1=row * 40
                canvas.create_text(x1+20,y1+20, text="🚩",font=("Arial",12))
                
            elif(grid_content[row][col]["flagged"]==False and grid_content[row][col]["revealed"]==False):
                x1=col * 40
                y1=row * 40
                x2=x1 + 40
                y2=y1 + 40
                canvas.create_text(x1+20,y1+20, text=" ",font=("Arial",12))
                canvas.create_rectangle(x1,y1,x2,y2,fill="dark green")
            
            elif(grid_content[row][col]["revealed"]==False):
                x1=col * 40
                y1=row * 40
                x2=x1 + 40
                y2=y1 + 40
                canvas.create_rectangle(x1,y1,x2,y2,fill="dark green")
              
            elif(grid_content[row][col]["revealed"]==True and grid_content[row][col]["mine"] ==True):
                x1=col * 40
                y1=row * 40
                x2=x1 + 40
                y2=y1 + 40
                canvas.create_rectangle(x1,y1,x2,y2,fill="red")
                canvas.create_text(x1+20,y1+20, text="💣",font=("Arial",12))
                    
            elif(grid_content[row][col]["revealed"]==True and grid_content[row][col]["number"]==0):
                x1=col * 40
                y1=row * 40
                x2=x1 + 40
                y2=y1 + 40
                canvas.create_rectangle(x1,y1,x2,y2,fill="#8B4513")
                
            elif(grid_content[row][col]["revealed"]==True and grid_content[row][col]["number"] !=0):
                x1=col * 40
                y1=row * 40
                x2=x1 + 40
                y2=y1 + 40
                
                canvas.create_rectangle(x1,y1,x2,y2,fill="dark green")
                canvas.create_text(x1+20,y1+20, text=grid_content[row][col]["number"],fill="white",font=("Arial",12))

def win_check():
    return all(cell["revealed"] or cell["mine"] for row in grid_content for cell in row)   
    


def left_click(event):# left click
    global game_over
    col = event.x // spacing
    row = event.y // spacing
    print(row,col)
    if(grid_content[row][col]["mine"]==True):
        grid_content[row][col]["revealed"]=True
        game_over= True
        
    elif(grid_content[row][col]["number"]==0):
        flood_fill(col,row)
        
    elif(grid_content[row][col]["number"]!=0):
        grid_content[row][col]["revealed"]=True
    
    
def right_click(event):
    col = event.x // spacing
    row = event.y // spacing
    print("Right click")
    if(grid_content[row][col]["flagged"]==False):
        grid_content[row][col]["flagged"]=True
    elif(grid_content[row][col]["flagged"]==True):
        grid_content[row][col]["flagged"]=False
    

def flood_fill(col_f,row_f):# flood if the clicked cell is empty
    direction=[(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]
    if(grid_content[row_f][col_f]["revealed"]==True):
        return
    elif(grid_content[row_f][col_f]["number"]==0):
        grid_content[row_f][col_f]["revealed"]=True
        for dir_row, dir_col in direction:
            new_row, new_col= row_f+dir_row, col_f+dir_col
            if 0<=new_row<rows and 0<=new_col<cols: # checks boundary
                if(grid_content[new_row][new_col]["number"]==0): # Checks if neighbor cell contain mines
                    
                    flood_fill(new_col,new_row)
                elif(grid_content[new_row][new_col]["number"]!=0):
                    grid_content[new_row][new_col]["revealed"] = True
                    # x1=new_col * 40
                    # y1=new_row * 40
                    # x2=x1 + 40
                    # y2=y1 + 40
                    # canvas.create_rectangle(x1,y1,x2,y2,fill="blue") 


fills_mines()
calc_neighbor()
game_over=False
def run():
    render_grid()
    if  game_over:
        canvas.create_text(300,100, text="Game Over !!! \nYou revealed a mine",fill="white",font=("Arial",16))
        return
    if  win_check():
        canvas.create_text(300,100, text="You Win !!! \nYou identified all the mines",fill="white",font=("Arial",16))
        return
    
    root.after(200,run)   

root.bind("<Button-1>", left_click)
root.bind("<Button-3>", right_click)
root.after(200,run) 
root.mainloop()
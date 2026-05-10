# A simple tetris game using 2D array/list
from tkinter import *
import random


root =Tk()
root.title("Tetris")
shape_col=0
shape_row=0
current_row=0
current_col=3 # centers the spawning pieces and easierto move them
current_color="Red"
grid=[[0] * 10 for _ in range(20)] # makes 20 x 10 grid of 0's
shapes={
    "I-Shape":[
        [1,1,1,1]
    ],
    "L-Shape":[
        [1,0],
        [1,0],
        [1,1]
    ],
    "O-Shape":[
        [1,1],
        [1,1]
    ],
    "T-Shape":[
        [0,1,0],
        [1,1,1]
    ],
    "S-Shape":[
        [0,1,1],
        [1,1,0]
    ]   
}
color=["Red","Blue","Green","Orange","White","Yellow","Lime","Lightblue"]
  
current_shape=random.choice(list(shapes.values()))
#current_shape=shapes["I-Shape"]
canvas=Canvas(root,width=300, height=600,bg="black" )
canvas.pack()
def display():
    
    for row in range (20): #  y axis
        for col in range (10): # x axis
            if grid[row][col]!=0:
                x1=col* 30
                y1=row * 30
                x2=x1+30
                y2=y1+30
                canvas.create_rectangle(x1,y1,x2,y2,fill=grid[row][col])

def draw():
    global shape_col,shape_row,current_shape
    shape_row, shape_col=0,0
    row=len(current_shape)
    col = max(len(row) for row in current_shape)
    # Get dimension of shape
    shape_row=row 
    shape_col=col
    
def shape_spawn():
    global shape_row,shape_col,current_shape,current_row,current_col,random_color
    #spawn_point=[0][4]
     
    for row in range (shape_row): #  y axis
        for col in range (shape_col): # x axis
            if current_shape[row][col]==1:
                x1=(col+current_col)* 30
                y1=(row +current_row) * 30
                x2=x1+30
                y2=y1+30
                canvas.create_rectangle(x1,y1,x2,y2,fill=current_color)
                

def shape_fall():
    global current_row
    current_row+= 1

def collision_detection():
    hit=False
    global current_row, current_col,current_shape,shape_row,shape_col
    if(current_row+shape_row-1>=19):
        for row in range(shape_row):
            for col in range(shape_col):
                if current_shape[row][col]==1:
                    grid[row+current_row][col+current_col]=current_color
        return True    
    elif(current_row+shape_row-1<19):
        for row in range(shape_row):
            for col in range(shape_col):
                if current_shape[row][col]==1:
                    if(grid[row+current_row][col+current_col]!=0):
                        shape_lock()
                        hit=True
                    if(grid[row+current_row+1][col+current_col]!=0):
                        shape_lock()
                        hit=True
        if hit:
            return True
    print(current_row)
    shape_fall()
    
    
def shape_lock():
    global shape_row,shape_col,current_shape,current_row,current_col,current_color
    for row in range(shape_row):
            for col in range(shape_col):
                if current_shape[row][col]!=0:
                    grid[row+current_row][col+current_col]=current_color

def clears_line():
    for row in range(20):
        if(all(cell!=0 for cell in grid[row])):
            for i in range((row),0,-1):
                grid[i]=list(grid[i-1])
            grid[0]=[0,0,0,0,0,0,0,0,0,0]
            
            # grid[row]=[0]* 10

draw() 
def game_over_check():
    global current_col,current_row,current_shape
    game_over=False
    for row in range(shape_row):
        for col in range(shape_col):
            if current_shape[row][col] == 1:
                if(grid[row+current_row][col+current_col]!=0):
                        game_over=True
    if game_over:
        return True                        
def game_run():
    global current_row, current_col,current_shape,shape_row,shape_col,current_color
    
    canvas.delete("all")
    display()
    shape_spawn()
    if game_over_check():
        canvas.delete("all")
        canvas.create_text(150,300,text="Game Over",font=("Arial",16),fill="white")
        return
    if collision_detection():
        # new function that handle shape spawning and re initializes position
        random_color=random.choice(color) 
        current_color=random_color
        shape_col=0
        shape_row=0
        current_row=0
        current_col=3
        current_shape=random.choice(list(shapes.values()))
        clears_line()
 
        draw()
    root.after(200, game_run)

# Shape moving and rotating logic
def move_left(event):
    global current_row,current_col
    if(current_col<1):
        return
    for row in range(shape_row):
        for col in range(shape_col):
            if current_shape[row][col]==1:
                if grid[current_row+row][col+current_col-1]!=0:
                    return
              
    current_col-=1
def move_right(event):
    global current_row, current_col, shape_col
    if current_col+shape_col-1 >= 9:
        return
    for row in range(shape_row):
        for col in range(shape_col):
            if current_shape[row][col] == 1:
                if grid[current_row+row][col+current_col+1] != 0:
                    return
    current_col += 1
def rotate(event):  
    global current_row,current_col,current_shape
    overlap= False
    old_shape=current_shape
    current_shape=[list(row) for row in zip(*current_shape)]
    new_col=max(len(row) for row in current_shape)
    new_row=len(current_shape)
    if current_col+new_col-1>=9 or current_col<0 or current_row+new_row-1>=19:
        current_shape=old_shape
        return
    
    for row in range(new_row):
        for col in range(new_col):
            if grid[row+current_row][col+current_col]!=0:
                overlap=True
    
    if overlap:
        current_shape=old_shape
    else:
        draw()
    
    
def move_down(event):
    global current_row, current_col
    if current_row+shape_row-1 >= 19:
        return
    for row in range(shape_row):
        for col in range(shape_col):
            if current_shape[row][col] == 1:
                if grid[current_row+row+1][col+current_col] != 0:
                    return
    current_row += 1
# bind key to keyboard
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<Up>", rotate)

root.bind("<Down>", move_down)
               
root.after(200,game_run)
root.mainloop()
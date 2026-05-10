from tkinter import *
import random
root = Tk()
root.title("Apple eater")
canvas =Canvas(root, width=400, height=400, bg= "black")
canvas.pack()
# creating rectnagle
x=0

snake = [(10,10),(9,10),(8,10)]
direction=[1,0] # defining an empty list to store col and row as direction
curr_direction=[1,0]
apple_position=()
score=0

def apple_spawn():
    global apple_position
    apple_posx=random.randint(0,19)
    apple_posy=random.randint(0,19)
    ax1=apple_posx*20
    ay1=apple_posy*20
    ax2=ax1+20 
    ay2=ay1+20
    apple_position=(apple_posx,apple_posy)
    canvas.create_oval(ax1, ay1, ax2, ay2, fill="red")
apple_spawn()    
    
def move():
    global curr_direction
    global apple_position
    global score
    canvas.delete("all")
    canvas.create_rectangle(2,2,400,400,fill="black")
    canvas.create_text(50, 10,text=f"Score: {score}",fill="white",font=("Arial",14))
    
    # respawing apple in same place
    apple_posx,apple_posy=apple_position
    ax1=apple_posx*20
    ay1=apple_posy*20
    ax2=ax1+20 
    ay2=ay1+20
    canvas.create_oval(ax1, ay1, ax2, ay2, fill="red")
    
       
    COL, ROW=snake[0]
    
    dir_x,dir_y=direction
    c_dx,c_dy=curr_direction
    # print(c_dx, c_dy, dir_x, dir_y)
    # Direction restriction logic
    if(c_dx==-(dir_x) and c_dy==-(dir_y)):
        new_head=(COL+c_dx,ROW+c_dy)
        snake.insert(0,new_head) 
    
        
        if(apple_position==new_head):
            apple_spawn()
            score=score+1
        else:
            snake.pop()   
      
    else:
        new_head=(COL+dir_x,ROW+dir_y)
        snake.insert(0,new_head) 
        
        curr_direction=direction[:]
        if(apple_position==new_head):
            apple_spawn()
            score=score+1
        else:
            snake.pop()
    # checks if snake touched the border, Border touch logic
    new_col,new_row=new_head
    if (new_col<0 or new_col> 19 or new_row <0 or new_row>19):
        canvas.create_text(200,200,text=f"Game Over!!!\n Score:{score}",fill="White", font=("Arial",16))
        return
    
    if new_head in snake[1:]:
        canvas.create_text(200,200,text=f"Game Over!!!\n Score:{score}",fill="White", font=("Arial",16))
        
        return
    # Renders the snake    
    
    for col, row in snake:    
        x1 = col * 20
        y1 = row * 20
        x2 = x1 + 20
        y2 = y1 + 20

        canvas.create_rectangle(x1, y1, x2, y2, fill="green")
    
    root.after(200,move)    


# apple spawning function

    
    
# Rectangle moving function
def move_left(event):
    global direction
   
    direction=[-1,0]
  
    return
def move_right(event):
    global direction
    
    direction=[1,0]
    
def move_down(event):
    global direction
    
    direction=[0,1]
    
def move_up(event):
    global direction
    
    direction=[0,-1]
    

# bind key to keyboard
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<Up>", move_up)
root.bind("<Down>", move_down)

root.after(200, move)
root.mainloop()

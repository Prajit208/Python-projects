# A simple pong game played against computer
from tkinter import *
root=Tk()
root.title("Pong")
direction=[]
y_pos_player=500
y_pos_computer=500
x_pos_ball,y_pos_ball=400,400
ball_direction=[(20,10)]
slider2_position=[]
score1=0
score2=0

canvas=Canvas(root, width=600, height=600,bg="black")
canvas.pack()
def slider():
    global y_pos_player,slider2_position,slider1_position
    canvas.create_rectangle(0,y_pos_computer,20,y_pos_computer+100,fill="white")
    canvas.create_rectangle(580,y_pos_player,600,y_pos_player+100,fill="white") # Player's slider
    slider2_position=[(580,y_pos_player),(600,y_pos_player+100)]
    slider1_position=[(0,y_pos_computer),(20,y_pos_computer+100)]
    canvas.create_text(50,20,text=f"Score: {score1}",font=("Arial",12))
    canvas.create_text(500,20,text=f"Score: {score2}",font=("Arial",12))
    
def ball():
    global x_pos_ball, y_pos_ball,ball_direction, score1,score2
    x,y=0,0
    
    x,y=ball_direction[0]
    #wall bounce function
    if(y_pos_ball<1 or y_pos_ball>580):
        y=y * -1
        ball_direction=[(x,y)]
    
    # ball bouncing function
     # 4 cases
    '''
    if direction(+,+)-> hits right paddle -> new direction= (-,+)
    if direction(+,-)-> hits right paddle -> new direction= (-,-)
    if direction(-,+)-> hits left paddle -> new direction= (+,+)
    if direction(-,-)-> hits left paddle -> new direction= (+,-)
    
    '''
    # paddle collision
    score_display()
    computer_paddle_logic()
    # scoring function
    if(x_pos_ball<=1):
        if(y_pos_ball>=y_pos_computer and y_pos_ball<=y_pos_computer+100):
            if(x<0):# ball moving right
                x=x*-1 
                ball_direction = [(x, y)]
                print("left paddle ")
                print(x)
        else:
            score2=score2+1
            x=20
            y=10
            print(" left paddle esle else is running")
            ball_direction=[(x,y)]
    
            x_pos_ball=290
            y_pos_ball=290
        
    if(x_pos_ball+20>=600):
        if(y_pos_ball>=y_pos_player and y_pos_ball<=y_pos_player+100):
            if(x>0):# ball moving right
                x=x*-1
                ball_direction = [(x, y)]
                print("right paddle")
                print(x)    
            
                
        else:
            x_pos_ball=600
            score1=score1+1
            x=-20
            y=-10
            print(" right paddle else running")
            ball_direction=[(x,y)]
    
            x_pos_ball=290
            y_pos_ball=290
        
                  
    x_pos_ball=x_pos_ball+x
    y_pos_ball=y_pos_ball+y
    # ball_position=[(x_pos_ball,y_pos_ball),(x_pos_ball+20,y_pos_ball+20)]
    
    # if ball_position in slider2_position:
    #     ball_direction=[(-20,-10)]
    # if(y_pos_ball<1):
    #     return

    canvas.create_oval(x_pos_ball,y_pos_ball,x_pos_ball+20,y_pos_ball+20,fill="orange")  
    
def computer_paddle_logic():
    global y_pos_computer,slider1_position
    y_pos_computer=y_pos_ball-50
    
def score_display():
    global score1,score2
    canvas.create_text(50,20,text=f"Score: {score1}",fill="white",font=("Arial",12))
    canvas.create_text(500,20,text=f"Score: {score2}",fill="white",font=("Arial",12))
def game_run():
    canvas.delete("all")
    slider() 
    ball()
    score_display()
    root.after(50,game_run)
    
def move_up(event):
    global y_pos_player
    y_pos_player=y_pos_player-20
def move_down(event):
    global y_pos_player
    y_pos_player=y_pos_player+20
root.bind("<Up>", move_up)
root.bind("<Down>", move_down)  
root.after(50,game_run)
root.mainloop()
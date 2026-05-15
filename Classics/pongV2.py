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
x,y=0,0
WINSCORE=5
game_started=False

canvas=Canvas(root, width=600, height=600,bg="black")
canvas.pack()
def slider():
    global y_pos_player,slider2_position,slider1_position
    
    for i in range(0, 600, 20):  # every 20px, draw a small dash
        canvas.create_line(300, i, 300, i+10, fill="white", dash=(4,10))
    

    canvas.create_rectangle(0,y_pos_computer,20,y_pos_computer+100,fill="white") # Computer's Paddle
    canvas.create_rectangle(580,y_pos_player,600,y_pos_player+100,fill="white") # Player's Paddle
    slider2_position=[(580,y_pos_player),(600,y_pos_player+100)] # Player's paddle position
    slider1_position=[(0,y_pos_computer),(20,y_pos_computer+100)] # Computer paddle position
    

        
def scoring():
    global x,y, ball_direction,x_pos_ball,y_pos_ball,score1,score2
    
    if(x_pos_ball<=0):
        score2+=1
        x,y=20,10
        ball_reset()
        
    if(x_pos_ball>=600):
        score1+=1
        x, y = -20, 10 
        ball_reset()  
               
def ball_reset():
    global ball_direction,x_pos_ball,y_pos_ball
    ball_direction=[(x,y)]
    x_pos_ball=290
    y_pos_ball=290
       
def ball():
    global x_pos_ball, y_pos_ball,ball_direction, score1,score2,x,y
    x,y = ball_direction[0]
    print(x_pos_ball, y_pos_ball)
    score_display()
    computer_paddle_logic()
    wall_bounce()
    paddle_collision_logic()
    scoring()
    
    
    x_pos_ball=x_pos_ball+x
    y_pos_ball=y_pos_ball+y
    
    canvas.create_oval(x_pos_ball,y_pos_ball,x_pos_ball+20,y_pos_ball+20,fill="orange")  
    
def computer_paddle_logic():
    global y_pos_computer,slider1_position
    target=y_pos_ball-50
    
    if y_pos_computer < target:
        y_pos_computer += 10
    elif y_pos_computer > target:
        y_pos_computer -= 10
    
def paddle_collision_logic():
    global ball_direction,x,y,x_pos_ball,y_pos_ball,y_pos_computer,y_pos_player
    if(x_pos_ball<=20):
        if(y_pos_ball>=y_pos_computer and y_pos_ball<=y_pos_computer+100):
            if(x<0):# ball moving right
                x=x*-1 
                ball_direction = [(x, y)]
                
        
    if(x_pos_ball>=560):
        # print(y_pos_ball, y_pos_player, y_pos_player+100)
        if(y_pos_ball>=y_pos_player and y_pos_ball<=y_pos_player+100):
            
            if(x>0):# ball moving right
                x=x*-1
                ball_direction = [(x, y)]
                print("right paddle")
                print(x)    
                 

def wall_bounce():
    # defines when ball touches top and bottom of game window
    global x,y, ball_direction,x_pos_ball,y_pos_ball
    
    if(y_pos_ball<1 or y_pos_ball>580):
        y=y * -1
        ball_direction=[(x,y)]            
     
def score_display():
    global score1,score2
    canvas.create_text(50,20,text=f"Score: {score1}",fill="white",font=("Arial",12))
    canvas.create_text(500,20,text=f"Score: {score2}",fill="white",font=("Arial",12))
def check_winner():
    
    global score1,score2,WINSCORE
    if score1==WINSCORE:
        canvas.create_text(300,300,text=f"Computer won!!! \nComputer's Score:{score1}\nPlayer's Score: {score2}",fill="white",font=("Arial",16))
        return True
    if score2==WINSCORE:
        canvas.create_text(300,300,text=f"Player won!!!\nPlayer's Score:{score2}\nComputer's Score: {score1}",fill="white",font=("Arial",16))
        return True
    return False

def start_game():
    global game_started
    game_started=True
    start_button.pack_forget()
    game_run()
    
   
def game_run():
    canvas.delete("all")
    if check_winner():
        return
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
    
start_button=Button(root, text="Start Game",command=start_game,font=("Arial",16),fg="white",bg="black")
start_button.pack()
    
root.bind("<Up>", move_up)
root.bind("<Down>", move_down)  
# root.after(50,game_run)
root.mainloop()
import pygame
pygame.init()
from collections import deque
running=True

ROWS=20
COLS=20
WIDTH=600
HEIGHT=600
CELL=30
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pathfinding visualizer")
mode="wall"

grid=[["empty" for _ in range(COLS)] for _ in range(ROWS)]
print(grid)
def get_cell(x,y):
    col=x//CELL
    row=y//CELL
    return row,col
clock=pygame.time.Clock()
def find_start():
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col]=="start":
                return row,col
    return None            
def find_end():
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col]=="end":
                return row,col
    return None  
def bfs():
    start=find_start()
    end=find_end() 
    queue= deque()  # doubel ended queue
    queue.append(start) 
    visited_cell=set()# set so same cell dont get counted twice
    visited_cell.add(start)
    came_from={}    
    while queue:# loops until queue empties
        current=queue.popleft() # gets the first element in queue
        if current=="end":
            break
def handle_click(x,y,button):
    global mode
    row,col= get_cell(x,y)
    
    if button == 1:
        grid[row][col] = mode
    if button == 3:
        grid[row][col] = "empty"
    
    
    
    
            
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(*pygame.mouse.get_pos(), event.button)
        if event.type==pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                handle_click(*pygame.mouse.get_pos(),1)
            if pygame.mouse.get_pressed()[2]:
                handle_click(*pygame.mouse.get_pos(),3)
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_s:
                mode="start"
            if event.key==pygame.K_e:
                mode="end"
            if event.key==pygame.K_w:
                mode="wall"
    screen.fill((255,255,255))# White fill 
    
    # Display
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col]=="wall":
                pygame.draw.rect(screen,(0,0,0),(col*CELL,row*CELL,CELL,CELL))
            if grid[row][col]=="start":
                pygame.draw.rect(screen,(0,255,0),(col*CELL,row*CELL,CELL,CELL))
            if grid[row][col]=="end":
                pygame.draw.rect(screen,(255,0,0),(col*CELL,row*CELL,CELL,CELL))
    
            
    
    for i in range(0,WIDTH,CELL):
        pygame.draw.line(screen,((0,0,0)),(i,0),(i,HEIGHT))
    for i in range(0,HEIGHT,CELL):
        pygame.draw.line(screen,((0,0,0)),(0,i),(WIDTH,i)) 
    pygame.display.flip()    
pygame.quit()    
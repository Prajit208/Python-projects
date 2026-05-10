# import random
# rows=5
# cols=15
# cell={
#     "mine": False,
#     "revealed": False,
#     "flagged": False,
#     "number": 0
# }
# grid_content=[[cell.copy()] * cols for _ in range(rows)]# cell.copy() makes copies of each dictionary so changing one doesnt chaneg other cell
# mine_count=5
# print(grid_content)
# # def fills_mines():
# #     mine_position=random.sample(range(rows* cols),mine_count)
# #     for pos in mine_position:
# #         row,col= divmod(pos,cols)
# #         grid_content[row][col]="mine"
# #     print(grid_content)  

piece_value={
        "Pawn": 1,
        "Knight":3,
        "Bishop": 3,
        "Rook":5,
        "Queen": 9,
        "King":1000
    }

print(piece_value["Bishop"])
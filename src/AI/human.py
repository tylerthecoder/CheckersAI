
def play(grid):
    
    click = grid.window.waitForClick()

    #if you click the piece that you already selected, then unselect
    if grid.selected == click:
        grid.selected = (-1,-1)

    #if you click your piece, then select it
    elif grid.board[click].color == grid.turn:
        grid.selected = click
    
    #try to play
    else:
        move = grid.makeMove(grid.selected,click)
        res = grid.checkMove(move)
        if res["valid"]: #if the move was sucsessful
            grid.selected = (-1,-1)
            return move
        else:
            print(res["error"])
            return False
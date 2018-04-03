# CheckersAI
An AI project where the goal is to have an AI beat a human at checkers

Note, The pygame library is required for this to work

To install pygame on your machine run the following python command

```
python3 -m pip install -U pygame --user
```

Now, to contribute to this project, try wrting your own AI!

# Functions
Here is an explination of all the major funcitons

## Board.getAllMoves
Input: player (string), [jumps = false] (bool)

This function will get all moves avaliable on a given board

The first parameter (player), specifies if whose moves you want to look for, either "r" (red player) or "b" (black player)

The second parameter is the jump flag, if true, it will only look for jumps, speeding up the searching process.

## Board.copy
Input: None

Output: A new board

Sample
```
newBoard = Board.copy()
```

This function takes the board you are using anc returns another board that has all the same data. Useful if you want to test moves and not mess up the main board

## Board.isRealSpot
Input: Tuple (x,y)
Output: True|False
Sample:
```
if board.isRealSpot((2,9)):
    #do something
else:
    #not a real spot
```
Used to tell is a spot is correct and is contained on the board

## Board.otherColor
Input: Player Color ("r","b")
Output: Other Player Color ("b","r")
Sample:
```
me = "r"
otherPlayer = Board.otherColor(me) #returns "b"
```
This returns the opposite color of a given color. Useful for checking things about your opponent


## Board.applyMove
Input:Move
Output:True|False

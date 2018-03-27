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



## Board.__init__
Input: type_of_board (string), [copy] (Board)

There are two boards that will be most usefull

    StandardBoard = Board("Standard")
This will create just the normal starting board

    CopyedBoard = Board("Copy",AnotherBoard)
    
This will copy the entire board over to another variable. This is useful is you are trying to check a move without altering the real board

## Board.getAllMoves
Input: player (string), [jumps = false] (bool)

This function will get all moves avaliable on a given board

The first parameter (player), specifies if whose moves you want to look for, either "r" (red player) or "b" (black player)

The second parameter is the jump flag, if true, it will only look for jumps, speeding up the searching process.

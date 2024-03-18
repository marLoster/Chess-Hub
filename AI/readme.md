There where many attempts to train succesful chess bots however the task seems pretty difficult so there is still a lot of work to do.

The general approach is to use neural networks to predict next move based on a given board.
Board is encoded using 12x8x8 array which contains 12 chess boards each filled with certain figure and color (first six boards are the bot pieces, the latter six belong to the opponent)
There are models with different outputs:
  board_models - return 2 boards - on the first one the piece they wish to move is selected, on the second one the square they want to move the piece to is selected.
    Since they return full boards with probabilities for each square, the expected move is either calculated by max scores of each board (bot Max) or by harmonic means of corresponding squares (bot Henry).
    Bot Rachel generates random moves, it does not need trained nn.
    Max and Henry use custom loss function since the boards they predict are sparsly populated matrices.

  value_models (Victor) - These models predict how good current board is for them. To select a move they explore all possible moves and select the one for which predicted value is the highest.
  Values for training set were calculated based on custom function that gives positive values if the game was eventually won, and negative if it was lost. The closer to the end, the higher values are given to the board. 
  There are also bonus points for making a check.

  Victor2 is a better version of Victor that will almost always prefer to check the opponent, however this is implemented by simple if-else statements.


TODO:
  - increase model complexity
  - try new nn layers, models, custom loss functions
  - acquire more data for training

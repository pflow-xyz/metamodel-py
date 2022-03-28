import metamodel

import examples.counter
import examples.pointer
import examples.tictactoe

# Counter model supports n++/n-- operations on a 2-n vector
Counter = metamodel.Model('counter_v1', examples.counter.v1)

# Pointer models create/update/disable operations on a named 'object'
Pointer = metamodel.Model('pointer_v1', examples.pointer.v1)

# play a game of tic-tac-toe
TicTacToe = metamodel.Model('tic_tac_toe', examples.tictactoe.v1)

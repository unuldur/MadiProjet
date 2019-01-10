=========== How to use Magic Maze ===========

The program is to be launched using python3
with the following command:

python3 main.py

Several options are used to select the 
features needed:

  -d D         dungeon file to play with
  -r R         size of random dungeon
  -s S         move speed in milliseconds
  -l L         starting life of the player 

  --pdmIteVal  Solve using Iteration Value
  --pdmGurobi  Solve using MIP and Gurobi
  --qLearn     Solve using QLearning

  --infinite   Solve until the first win

  --bench      Run the benchs and

  -h           show the help
  --help       show the help

Arguments' order does not matter.
If no resolution method is given, the moves
are given by the player.


Examples of utilisation:
 - Run Gurobi on a 12x12 random Dungeon

  python3 main.py -r 12 --pdmGurobi

 - Same with 4 lifepoint for the player

  python3 main.py -r 12 -l 4 --pdmGurobi

 - Keep runnning until a win

  python3 main.py -r 12 -l 4 --pdmGurobi -- infinite
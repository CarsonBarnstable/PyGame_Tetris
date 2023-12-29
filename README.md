# PyGame_Tetris
### A Self-Playing Tetris Game (built on PyGame)
#### Disclaimer:
This project was initially inspired by Lee Yiyuan and his [Tetris AI – The (Near) Perfect Bot](https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/).<br>All of the code is my own (unless otherwise indicated), but the project idea is inspired directly from here.
# How it Works:
#### This program is a basic Tetris clone, that has then added AI abilities. The pieces are placed according to five key objectives:
1) Maximize "Full Rows" *(the number of rows that will be converted into points once piece is placed)*
2) Minimize "Bumpiness" *(the total absolute differences in heights between adjacent columns in 'mass')*
3) Maximize "Distance to Top" *(the number of empty rows between the uppermost piece and the top of the grid)*
4) Minimize "Overhangs" *(the number of 'holes' in the mass that become inaccessible if piece is placed)*
5) Maximize "Percent Filled" *(the percentage of total space below the highest block, that is filled with other blocks)*
     - Note: this is impacted by the other 4 objectives, but can be used to fine-tune different sensitivities

These 5 objectives are all given a certain "weight", where a positive weight indicates a maximization objective, and a negative weight indicates a minimization objective.

#### When a (randomly selected) new piece is generated, the AI tries placing the new piece in every possible position, with every possible rotation. For each scenario:
1) The game is simulated, to see where the piece would fall (and therefore how the game would look if that move was chosen)
2) The number of Full Rows, the Bumpiness, Distance to Top, number of Overhangs, and Percent Filled are all calculated
3) A "drop score" is calculated by multiplying the previously-chosen coefficients by their respective statistic
4) The drop position/rotation is stored alongside the calculated score of choosing that drop

Once all the scenarios are simulated (and their scores calculated), the scenario with the highest score is chosen, the drop is performed (with the chosen position/rotation), and the game continues.

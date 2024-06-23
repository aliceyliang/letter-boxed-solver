# letter-boxed-solver

Letter Boxed Solver for the game from The New York Times.

### Overview
This is a small script to find solutions for the game Letter Boxed from The New York Times and store them maintaining a journal of the game and its solutions

### How it works
A user inputs the letters found from the game. The app looks for 1, 2, or 3 word solutions, depending on what is specified (4+ word solutions have too many permutations and makes this too slow). These solutions are made up of words whose characters can be found in the box but are not on adjacent sides. The set of words that make up a solution must use all the letters in the box. The app iterates through possible solutions from a word list in which those with repeated letters removed, resulting in `words_easy.txt` with ~84k words.
#### Credits
The original idea was based on [this Repl.it](https://repl.it/@demonpuncher/New-York-Times-Spelling-Bee-Puzzle-Solver) that provided a solver for Spelling Bee, another game from NYT. The shorter word list is from that solver. The longer word list is from [`@dwyl/english-words`](https://github.com/dwyl/english-words).

This has been improved upon to include more solutions and optimize for runtime to be fetched by GitHub Actions

#### Deployment
Deployed through GitHub actions and automations

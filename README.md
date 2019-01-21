# letter-boxed-solver

### Overview
This is a small Flask app to find solutions for the game Letter Boxed from The New York Times. Live site at [letterboxed.aliceyliang.com](https://letterboxed.aliceyliang.com).

### How it works
A user inputs the letters found from the game. The app looks for 1, 2, or 3 word solutions, depending on what is specified (4+ word solutions have too many permutations and makes this too slow). These solutions are made up of words whose characters can be found in the box but are not on adjacent sides. The set of words that make up a solution must use all the letters in the box. The app iterates through possible solutions through the qualifying words in `words.txt`, a list of ~110k English words. If none are found, it searches through `words_alpha.txt`, a list of ~370k words. If still no words are found, or if the user inputs incorrect letters, an error message appears. What's super fun is that if there is a solution, a "scratch-off" board appears on the right side and the user can move the mouse around to reveal the solutions.

#### Credits
The original idea was based on [this Repl.it](https://repl.it/@demonpuncher/New-York-Times-Spelling-Bee-Puzzle-Solver) that provided a solver for Spelling Bee, another game from NYT. The `words.txt` file is from that solver. The longer word list, `words_alpha.txt`, is from [`@dwyl/english-words`](https://github.com/dwyl/english-words).

The scratch off element was inspired by the first lesson in [SuperHi's Experimental JavaScript class](https://www.superhi.com/courses/experimental-javascript). This allows the user to reveal just part of the answer so they can keep on playing.

#### Deployment
Deployed through Google App Engine with a custom subdomain.

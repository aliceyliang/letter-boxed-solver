# letter-boxed-solver

Letter Boxed Solver for the game from The New York Times.

### Overview
This is a small Flask app to find solutions for the game Letter Boxed from The New York Times. Live site at [letterboxed.aliceyliang.com](https://letterboxed.aliceyliang.com).

### How it works
A user inputs the letters found from the game. The app looks for 1, 2, or 3 word solutions, depending on what is specified (4+ word solutions have too many permutations and makes this too slow). These solutions are made up of words whose characters can be found in the box but are not on adjacent sides. The set of words that make up a solution must use all the letters in the box. The app iterates through possible solutions from a word list in which those with repeated letters removed, resulting in `words_easy.txt` with ~84k words. If none are found, it searches through a longer word list and removes words with repeated letters to get `words_hard.txt`, with ~286k words. If still no words are found, or if the user inputs incorrect letters, an error message appears. What's super fun (though not on mobile) is that if there is a solution, a "scratch-off" board appears on the right side and the user can move the mouse around to reveal the solutions.

#### Credits
The original idea was based on [this Repl.it](https://repl.it/@demonpuncher/New-York-Times-Spelling-Bee-Puzzle-Solver) that provided a solver for Spelling Bee, another game from NYT. The shorter word list is from that solver. The longer word list is from [`@dwyl/english-words`](https://github.com/dwyl/english-words).

The scratch off element was inspired by the first lesson in [SuperHi's Experimental JavaScript class](https://www.superhi.com/courses/experimental-javascript). This allows the user to reveal just part of the answer so they can keep on playing.

#### Deployment
Deployed through Google App Engine with a custom subdomain.

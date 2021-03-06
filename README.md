# Mastermind: The Game
**Project for INF1340: Intro to Programming**

Mastermind is a code breaking game where one player creates a short code (of either colours or numbers) and another play has a certain number of attempts to guess the correct code. The guesser provides feedback with Red or White pegs. White pegs represent a number that is in the code but not in the correct position, and Red pegs represent a number that is in the correct position. 

**Installations**
Users need to install the _itertools_ and _collections_ packages before the program can import and run smoothly. Upon the first successful running of the code the **play()** function will begin for users to play Mastermind, followed by **codeBreak()** which is intended to show how an algorithm breaks a code (can be the code just ran in **play()**). These can be commented in or out depending on how the user wants to ineract with the code.

**Main Functions**
The Mastermind Game and Solver.py/.ipynb files contains two parts (they are identical code). After initiating the code, running the **play()** function will begin a game of Mastermind against the computer. A random code is generated and players allow themselves a certain number of attempts to guess the correct code. 
<img width="751" alt="Screen Shot 2021-11-09 at 4 35 26 PM" src="https://user-images.githubusercontent.com/80587489/141008701-4fc44a88-de58-4463-9e1c-12bf53e5fa26.png">

The other part is the **codeBreak()**, which accepts a code from the user and an algorithm breaks it while printing it's guesses, feedback received, and the number of attempts it took. The majority of this code was adapted from [here](https://www.reddit.com/r/learnpython/comments/k07mfi/mastermind_game_solve_puzzles_optimal_moves_how/).

<img width="338" alt="Screen Shot 2021-11-09 at 4 39 21 PM" src="https://user-images.githubusercontent.com/80587489/141009203-3819b01b-0a3d-4315-b659-1dc5894711e0.png">

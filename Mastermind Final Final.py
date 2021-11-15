#!/usr/bin/env python
# coding: utf-8

# In[12]:


import numpy as np
import itertools
import collections


def listToInt(list):
    s = [str(i) for i in list] # Convert integer list to string list
    retInt = int("".join(s)) # Join list items using join()
    return(retInt)

def intToList(num):
    retInt = [int(x) for x in str(num)] # use list comprehension to convert number to list of integers
    return(retInt)

def firstPosMatch(code,guessItem, length):
    for i in range(0, length): 
        if code[i] == guessItem:#Look through both to find the first match, return the index of the match
            return i
def inStrToInt(prompt):
    while True:
        try:
            return int(input(prompt)) #Try to make int of the input
        except ValueError:
            print("I didn't understand that, please only input integers.") #Get mad if it can't be an int and ask again
            continue
        else:
            break
            
def play():
    #Instructions
    print("Red means a correct digit in the correct position.")
    print("White means a correct digit in the wrong position.")
    print("Numbers range from 1-6 to match Materminds 6 colours.")

    #Initial Inputs
    pSize=inStrToInt('What sized puzzle would you like(2-7)?:')
    tries=inStrToInt('How many tries would you like?:')

    #Create puzzle code
    solution=np.random.randint(1,6,size=pSize).tolist()

    while tries>0:
        numAndSpot=0 #Reset index of full matches
        justNum=0 #Reset index of num matches
        solveTry=solution.copy() #Make a new copy of the solution to modify
        guess=inStrToInt(f'Please input a guess ({tries} attempts left):') #Guess input
        guessList=intToList(guess) #Turn int guess to list
        if len(guessList)!= pSize:
            print(f'Guess must be {pSize} digits long') #Get mad and re-ask if the lengths of guesses and codes don't match
            continue
        else:
            for i in range(0,len(guessList)): #Iterate through guess
                if solveTry[i]==guessList[i]: 
                        numAndSpot += 1 #Add 1 to the full match count 
                        #Change values to not interfere with the next for loop
                        solveTry[i]=''
                        guessList[i]='-'

            for i in range(0,len(guessList)):
                if guessList[i] in solveTry:
                        justNum += 1 #Add one to just num match count
                        matchedPosition= firstPosMatch(solveTry,guessList[i],pSize) #Identify the first match position
                        #Change the values so values aren't counted more than once (very particular Mastermind rule)
                        solveTry[matchedPosition]=''
                        guessList[i]='-'

        #End game if solution is found
        if numAndSpot==pSize:
            print(f'''Congrats! You found the correct solution of {listToInt(solution)}!''')
            break
        tries-=1 #Reduce try count so the game evenutally ends
        print(f'White:{justNum} Red:{numAndSpot}') #Provide feedback following Mastermind rules

        #Let player know when they run out of tries/game is over
        if tries==0:
            print(f'''Nice try! The correct solution was {listToInt(solution)}!''') 


#Much of the following code was adapted from https://www.reddit.com/r/learnpython/comments/k07mfi/mastermind_game_solve_puzzles_optimal_moves_how/
Feedback = collections.namedtuple('Feedback', ['correct', 'close'])

def get_possible_feedback(holes):
    #Provides a range of feedback to compare to
    for n in range(holes+1):
        for i in range(holes+1-n):
          yield Feedback(n,i)


def generate_initial_pool(choices, holes):
    #Generates the initial set of possible answers
    return list(itertools.product(*[list(range(choices)) for _ in range(holes)]))


def find_correct(actual, guess):
    #Finds the sum of all correct matches.
    return sum([1 for (a, b) in zip(actual, guess) if a == b])


def remove_correct(actual, guess):
    #Removes all correct matches from two "rows"
    actual2 = [a for (a, b) in zip(actual, guess) if a != b]
    guess2 = [b for (a, b) in zip(actual, guess) if a != b]
    return actual2, guess2

def find_close(actual, guess):
    #Finds the sum of all close matches
    actual, guess = remove_correct(actual, guess)

    close = 0
    for possible in guess:
        if possible in actual:
            del actual[actual.index(possible)]
            close += 1
    return close

def get_feedback(actual, guess):
    #Compares two "rows" to each other and returns feedback
    return Feedback(find_correct(actual, guess), find_close(actual, guess))

def add_feedback(actual,guess):
    #Turns feedback into strings
    feedback=get_feedback(actual,guess)
    return str(feedback.correct)+str(feedback.close)

def filter_feedback(pool, guess,):
    #Compares feedback to others others in the pool
    for possible in pool:
        yield get_feedback(possible,guess)

def is_match(guess, feedback, possible):
    #Returns true if hypothetical could be the answer given the feedback and the guess
    return feedback == get_feedback(possible, guess)


def filter_pool(pool, guess, feedback):
    #Filters through the pool of possibilities and removes ones which couldn't possibly be the answer
    for possible in pool:
        if is_match(guess, feedback, possible): #and (possible != guess):

            yield possible


def make_guess(pool, orgpool):
    #Makes an educated guess between the pool of possibilities and feedback
    test={}
    best_choice = None
    max_score=0
    i=0
    for guess in orgpool: 
      test[guess]={}
      for possible in pool:
        feedback=add_feedback(possible,guess)
        if (feedback in test[guess]):
            test[guess][feedback]+=1
        else:
            test[guess][feedback]=1
      max_length=0
      for item in test[guess]:
        length=test[guess][item]

        if max_length < length:
            max_length = length
            score=len(pool)-max_length
            if score<max_score:
                break
            else:
                max_score=score
                best_choice=guess

    return best_choice

def codeBreak():
    #Function to solve any input code
    solution=intToList(inStrToInt(f'Please input a code (3-5) digits for breaking:'))
    
    choices = 7 #Provides range of values (0-6)
    holes = len(solution) #holes=positions
    print ('')

    pool = generate_initial_pool(choices, holes) #Create all possibilities
    pool = [i for i in pool if i and (0 not in i)] #Remove possibilites with 0 to match 1-6
    #print(pool)
    orgpool=pool.copy()
    somefeedback=list(get_possible_feedback(holes))
    attempts=1

    guess = [1 if (i < (holes / 2)) else 2 for i in range(holes)] #Initial guess

    while True:

        if len(pool)==1:
            guess=pool[0]
        numAndSpot=0 #Reset index of full matches
        justNum=0 #Reset index of num matches
        solveTry=solution.copy()
        guessList=list(guess)
        
        for i in range(0,len(guessList)): #Iterate through guess
            if solveTry[i]==guessList[i]: 
                    numAndSpot += 1 #Add 1 to the full match count 
                    #Change values to not interfere with the next for loop
                    solveTry[i]='.'
                    guessList[i]='-'
                    
        for i in range(0,len(guessList)):
            if guessList[i] in solveTry:
                    justNum += 1 #Add one to just num match count
                    matchedPosition= firstPosMatch(solveTry,guessList[i],holes) #Identify the first match position
                    #Change the values so values aren't counted more than once (very particular Mastermind rule)edf
                    solveTry[matchedPosition]='.'
                    guessList[i]='-'
        #Outputs just for observers
        print(guess)
        print(f'White:{justNum} Red:{numAndSpot} Attempt: {attempts}')
        
        print('')

        #Create and provide feedback automatically
        correct = numAndSpot
        close = justNum

        feedback = Feedback(correct, close)
        if feedback.correct == holes:
            break
        pool = list(filter_pool(pool, guess, feedback))
        
        attempts+=1 #Iterate attempts
        if len(pool)>1:
            print ("{0} possible choices left. Thinking...\n".format(len(pool)))
        else:
            print("1 possible choice left. Thinking...\n")
        orgpool.remove(tuple(guess)) #Remove guess from pool
        guess = make_guess(pool,orgpool) #Make new guess


play()
codeBreak()


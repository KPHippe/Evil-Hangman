import random

"""
Kyle Hippe
Fall 2018
11/5/2018
Python documentation, tutorialspoint.com for syntax help
Built using python3
"""
debug = 0
easymode = False
dictionary = {}
fam = list()
play = 1
printWrd = ""
guessed = False


def setdictionary():
    with open('dictionary.txt') as f:
        line_num = 1
        for line in f:
            line = line.rstrip()
            # key, value try to make it a list as the values
            if len(line) in dictionary:
                dictionary[len(line)].append(line)
            else:
                dictionary[len(line)] = list()
                dictionary[len(line)].append(line)
            line_num += 1


def firstfam(size):
    if size in dictionary:
        for x in range(len(dictionary[size])):
            fam.append(dictionary[size][x])
    else:
        size = int(input("No words of that length, please enter number less than 29 "))
        firstfam(size)


def nfamily(guess):
    # positions is a dictionary of the indexes of the guess and the number of words in that family
    positions = dict()
    largestFamPoition = dict()
    temp = -2
    positionList = list()

    # if fam size == 2 choose other fam always
    '''
    if len(fam) == 2:
        for x in fam:
            if x.find(guess):
                fam.remove(x)
                positionList.append(findOccurrences(fam[0], guess))
                return positionList
    '''

    # find positions of guess and figure out how many there are
    for x in fam:
        # position is the indexes of the guess
        charPosition = findOccurrences(x, guess)
        if len(charPosition) == 0:
            charPosition.append(-1)

        # cannot iterate over list, must be a tuple
        positionTup = tuple(charPosition)

        if positionTup in positions:
            positions[positionTup] += 1
        else:
            positions[positionTup] = 1

    # find largest famly from dictionary built above
    for x in positions:
        if positions[x] > temp:
            temp = positions[x]
            positionList = x

    # update family
    # need to create a copy of the list to properly iterate over

    famCpy = list(fam)
    for x in famCpy:
        if positionList[0] == -1:
            if x.find(guess, 0) != -1:
                fam.remove(x)
        elif list(findOccurrences(x, guess)) != list(positionList):
            fam.remove(x)

    if debug:
        print(fam)

    return positionList


def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

# guess is char, position is list, word is string
def printWord(guess, position, word):
    temp = list(word)
    if -1 not in position:
        for x in range(len(position)):
            temp[position[x] * 2] = guess

    return "".join(temp)

def printFirstWord(size):
    temp = ""
    for x in range(size):
        temp += "_ "

    return temp

def randWord(guess):
    if len(fam) > 1:
        temp = random.randint(0,len(fam))
        if not fam[temp].find(guess) == -1:
           randWord(guess)
    else:
        temp = random.randint(0, len(fam) - 1)
    return fam[temp]

def checkWordSize(size):
    if size in dictionary:
        return True
    else:
        return False
'''

start main method

'''
setdictionary()
if debug:
    print(dictionary)

while play:
    numGuesses = int(input("How many guesses would you like? "))
    while numGuesses < 0 or numGuesses > 26:
        numGuesses = int(input("Not a digit or valid guess number, please enter a number between 1 and 26 "))
    wordSize = int(input("What would you like the word length to be? "))
    while not checkWordSize(wordSize):
        wordSize = int(input("Size not in dictionary, please enter a different word length "))

    easyTemp = input("Would you like the word families to be displayed? Y/y = yes other = no ")
    if easyTemp == 'Y' or easyTemp == 'y':
        easymode = True
    else:
        easymode = False
    firstfam(wordSize)

    guess = input("Guess: ")
    # check if guess is a letter
    while not guess.isalpha():
        guess = input("Guess was not a letter, enter a letter: ")
    charsGuessed = list(guess)
    printWrd = printFirstWord(wordSize)

    for x in range(numGuesses-1):
        position = nfamily(guess)
        printWrd = printWord(guess, position, printWrd)
        print(printWrd)
        if position[0] == -1:
            print("Guess not in word!")
        # check if guessed
        if printWrd.find('_') == -1:
            print("Congratulations!")
            guessed = True
            playTemp = input("Would you like to play again? (Y/y = yes N/n = no)")
            if playTemp == 'y' or playTemp == 'Y':
                play = 1
            else:
                play = 0

            break
        if easymode:
            print(fam)
        print("You have guessed: ", charsGuessed)
        print("You have " + str(numGuesses - x-1) + " guesses left")
        guess = input("Guess: ")
        # check if a letter and if its already been guessed
        while not guess.isalpha():
            guess = input("Guess was not a letter, enter a letter: ")
        while guess in charsGuessed:
            guess = input("You have already guessed \'" + guess + "\', Please enter another charachter: ")

        charsGuessed.append(guess)
        # if its the last guess then it wont hit the top part of the loop and needs to be checked one
        # last time before exiting the loop, not the cleanest solution but it works
        if x == numGuesses - 2 and not guessed:
            position = nfamily(guess)
            printWrd = printWord(guess, position, printWrd)
            print(printWrd)
            if printWrd.find('_') == -1:
                print("Congratulations!")
                guessed = True
                playTemp = input("Would you like to play again? (Y/y = yes N/n = no)")
                if playTemp == 'y' or playTemp == 'Y':
                    play = 1
                else:
                    play = 0

    if not guessed:
        print("You did not guess the word!\n The word was: ", randWord(guess))
        playTemp = input("Would you like to play again? (Y/y = yes N/n = no)")
        if playTemp == 'y' or playTemp == 'Y':
            play = 1
        else:
            play = 0


if play == 0:
    print("Thank you for playing")


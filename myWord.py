#---------------------------------------------------------------#
#                       Wordle Game Solver
#                          version 1.0
#                         David McPhee
#                      written: Jan-29 2021
#---------------------------------------------------------------#
import sys
import time
# File Functions
def printSlow(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.01)

def getDefaultDic():
    return({'a': [0,0,0,0,0],
            'b': [0,0,0,0,0],
            'c': [0,0,0,0,0],
            'd': [0,0,0,0,0],
            'e': [0,0,0,0,0],
            'f': [0,0,0,0,0],
            'g': [0,0,0,0,0],
            'h': [0,0,0,0,0],
            'i': [0,0,0,0,0],
            'j': [0,0,0,0,0],
            'k': [0,0,0,0,0],
            'l': [0,0,0,0,0],
            'm': [0,0,0,0,0],
            'n': [0,0,0,0,0],
            'o': [0,0,0,0,0],
            'p': [0,0,0,0,0],
            'q': [0,0,0,0,0],
            'r': [0,0,0,0,0],
            's': [0,0,0,0,0],
            't': [0,0,0,0,0],
            'u': [0,0,0,0,0],
            'v': [0,0,0,0,0],
            'w': [0,0,0,0,0],
            'x': [0,0,0,0,0],
            'y': [0,0,0,0,0],
            'z': [0,0,0,0,0]})


def OpenFile(filename):
    with open(filename, "r") as abr:
        return(abr.read().split(','),abr)

def CloseFile(abr):
    abr.close()

## Check if word has duplicate letters
def CheckDup(listOfElems):
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True

def getGuess(attempt, lines):
## initialize values
    freq = getDefaultDic()
    score = {}

    dupPenalty = -1

    highestScore = 0
    highestWord = ""

    ## Determine Letter Freq
    for word in lines:
        ones = [1,1,1,1,1]
        word = word[1:6]
        for place in range(len(word)):
            freq[word[place]][place] += 1
               
    ## Rank Each word
    #   meth 1: score = sum of % of time a letter appears

    for word in lines:
        word = word[1:6]
        score[word] = 0
        letterIndex = 0
        
        # assign score
        for letter in word:
            score[word] += freq[letter][place]/len(lines)
            letterIndex += 1        
        if CheckDup(word):
            score[word] += dupPenalty
        

        # get highest score
        if score[word] > highestScore:
            highestScore = score[word]
            highestWord = word

    return highestWord
    
def modList(prevGuess,result,lines):
    newList = []
    blackLetters = []
    greenLetters = []
    yellowLetters = []

    ## Fill color lists
    for place in range(len(prevGuess)):
        if result[place] == "G":
            greenLetters.append((prevGuess[place],place))
        elif result[place] == "Y":
            yellowLetters.append((prevGuess[place],place))
            
    for place in range(len(prevGuess)):
        inOther = False
        if result[place] == "B":
            for yellowLetter in yellowLetters:
                if prevGuess[place] == yellowLetter[0]:
                    inOther = True
            for greenLetter in greenLetters:
                if prevGuess[place] == greenLetter[0]:
                    inOther = True
            if not inOther:
                blackLetters.append(prevGuess[place])
    ## Create shorter list
    for word in lines:
        word = word[1:6]
        remove = False
        place = 0
        for letter in word:
            ## Remove if a letter is black
            if letter in blackLetters:
                remove = True

            ## Remove if a letter is yellow
            if (letter, place) in yellowLetters:
                remove = True

            ## Remove if a letter isn't green
            for greenPair in greenLetters:
                if place == greenPair[1]:
                    if (letter, place) not in greenLetters:
                        remove = True

            place += 1
        ## Remove if a word doesn't contain all yellow letters
        for yellowLetter in yellowLetters:
            if yellowLetter[0] not in word:
                remove = True
        if not remove:
            newList.append('"'+word+'"')

    return newList        

        

## Terminal
lines, ml = OpenFile("myList.txt")
CloseFile(ml)

for attempt in range(1,7):
    if attempt == 1:
        guess = (getGuess(attempt,lines))
        printSlow("Welcome to Wordle Solver...\n")
        printSlow("Try this word first: \n" + guess.upper()+ "\n\n")
        printSlow("Did you use the recommended word? (Yes/No): ")
        ans = input().upper()
        if ans == "NO":
            printSlow("Which word did you try?: ")
            guess = input().upper()
        printSlow("Enter result (B)lack, (Y)ellow, or (G)reen (ex GBYBB): ")
        result = input().upper()
        printSlow("\n")
        shortLines = lines
        
    else:
        shortLines = modList(guess.lower(),result,shortLines)
        guess = (getGuess(attempt,shortLines))
        printSlow("Try this word: \n" + guess.upper()+"\n\n")
        printSlow("Did you use the recommended word?: ")
        ans = input().upper()
        if ans == "NO":
            printSlow("Which word did you try?: ")
            guess = input().upper()
        printSlow("Enter result: ")
        result = input().upper()
        printSlow("\n")

        if result == "GGGGG":
            printSlow("Good job, it took you " + str(attempt) +  " tries\n")
            printSlow("Goodbye!\n")
            break

















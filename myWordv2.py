#---------------------------------------------------------------#
#                       Wordle Game Solver
#                          version 2.2
#                         David McPhee
#                      written: Jan-29 2022
#                      updated: Feb-12 2022
#---------------------------------------------------------------#
#   Change log:
#   significant improvement to the logic of removing incorrect words
#   improvement to appearance and others
#   added option to change dic to pull words from
#   forced first word to be "Later"
#   made inputs more "user-proof"

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

def getGuess(attempt, lines):
## initialize values
    freq = getDefaultDic()
    score = {}

    highestScore = 0
    highestWord = ""

    ## Determine Letter Freq
    for word in lines:
        ones = [1,1,1,1,1]
        word = word[1:6]
        for place in range(len(word)):
            freq[word[place]][place] += 1
               

    #   meth 2: score = sum of % of time a letter appears

    for word in lines:
        word = word[1:6]
        score[word] = 0
        letterIndex = 0
        
        # assign score
        for letter in word:
            score[word] += sum(freq[letter])/(5*len(lines))
            if word.count(letter) > 1:
                score[word] /= word.count(letter)*5
            
            letterIndex += 1        

        # get highest score
        if score[word] > highestScore:
            highestScore = score[word]
            highestWord = word

    return highestWord
    
def modList(prevGuess,result,lines):
    newList = []
    blackLetters = []
    blackList = []
    greenLetters = []
    greenList = []
    yellowLetters = []
    yellowList = []
    result = result.upper()
    
    ## Fill color lists
    for place in range(len(prevGuess)):
        if result[place] == "G":
            greenList.append((prevGuess[place],place))
            greenLetters.append(prevGuess[place])
        elif result[place] == "Y":
            yellowList.append((prevGuess[place],place))
            yellowLetters.append(prevGuess[place])
        elif result[place] == "B":
            blackList.append((prevGuess[place],place))
            blackLetters.append(prevGuess[place])
            
    ## Create shorter list
    for word in lines:
        word = word[1:6]
        place = [0,1,2,3,4]
        wordList = tuple(zip(word, place))
        remove = False
        for greenCount in range(len(greenList)):
            if greenList[greenCount] not in wordList:
                remove = True

        for yellowCount in range(len(yellowList)):
            if yellowList[yellowCount] in wordList:
                remove = True
            if yellowList[yellowCount][0] not in word:
                remove = True

        for blackCount in range(len(blackList)):
            if  ((blackList[blackCount][0] not in yellowLetters) and
                (blackList[blackCount][0] not in greenLetters) and
                (blackList[blackCount][0] in word)):
                    remove = True
                        
            if blackList[blackCount] in wordList:
                remove = True
        
        if not remove:
            newList.append('"'+word+'"')

    return newList        

def getYN():
    invalid = True
    while invalid:
        ans = input().upper()
        if ans in ["NO","N"]:
            ans = "N"
            invalid = False
        elif ans in ["YES","Y"]:
            ans = "Y"
            invalid = False
        else:
            printSlow("Invalid response, please try again: ")
    return ans

def getW():
    invalid = True
    while invalid:
        ans = input().lower()
        if len(ans) == 5:
            invalid = False
        else:
            printSlow("Invalid response, please try again: ")
    return ans

def getR():
    invalid = True
    while invalid:
        bl = False
        ans = input().lower()
        for le in ans:
            if le in "acdefhijklmnopqrstuvwxz":
                bl = True
        if (len(ans) == 5) and (not bl):
            invalid = False 
        else:
            printSlow("Invalid response, please try again: ")
    return ans

def checkGuess(guess):
    if (guess == ""):
        printSlow("Welp either the hidden word is not in my word bank or you "+
                  "made a typo somewhere and lets just say my word bank is "+
                  "quite extensive\n")
        printSlow("Exiting...")
        quit()
    

## Terminal
lines, ml = OpenFile("myList.txt")
CloseFile(ml)

for attempt in range(1,70):
    if attempt == 1:
        guess = "Later"
        printSlow("Try this word first: \n" + guess.upper()+ "\n\n")
        printSlow("Did you use the recommended word? (Yes/No): ")
        ans = getYN()
        if ans == "N":
            printSlow("Which word did you try?: ")
            guess = getW()           
        printSlow("Enter result (B)lack, (Y)ellow, or (G)reen (ex GBYBB): ")
        result = getR()
        printSlow("\n")
        shortLines = lines

        
        
    else:
        shortLines = modList(guess.lower(),result,shortLines)
        guess = (getGuess(attempt,shortLines))
        checkGuess(guess)
        printSlow("Try this word: \n" + guess.upper()+"\n\n")
        printSlow("Did you use the recommended word?: ")

        ans = getYN()

        if ans == "N":
            printSlow("Which word did you try?: ")
            guess = getW()
        printSlow("Enter result: ")
        result = getR()
        printSlow("\n")

    if result.upper() == "GGGGG":
        printSlow("Good job, it took you " + str(attempt) +  " tries.\n")
        printSlow("Goodbye!\n")
        break

















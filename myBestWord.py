#---------------------------------------------------------------#
#                       Best Starting Word
#                          version 1.0
#                         David McPhee
#                      written: Feb-4 2022
#---------------------------------------------------------------#

import sys
import time
import copy
from myAutoWord import *

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
               
    ## Rank Each word
    #   meth 1: score = sum of % of time a letter appears

##    for word in lines:
##        word = word[1:6]
##        score[word] = 0
##        letterIndex = 0
##        
##        # assign score
##        for letter in word:
##            score[word] += freq[letter][place]/len(lines)
##            if word.count(letter) > 1:
##                score[word] /= (word.count(letter) + 1)
##            
##            letterIndex += 1        
##
##        # get highest score
##        if score[word] > highestScore:
##            highestScore = score[word]
##            highestWord = word

    #   meth 2: score = sum of % of time a letter appears

    for word in lines:
        word = word[1:6]
        score[word] = 0
        letterIndex = 0
        
        # assign score
        for letter in word:
            score[word] += sum(freq[letter])/(5*len(lines))
            if word.count(letter) > 1:
                score[word] /= (word.count(letter))*4
            
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

        

## Terminal
lines, ml = OpenFile("myList.txt")
CloseFile(ml)
metaLines, ml = OpenFile("myMeta.txt")
CloseFile(ml)
startingLines, ml = OpenFile("myStart.txt")
CloseFile(ml)

bestScore = 100
bestWord = ""
timer = 100
for startingWord in startingLines:
    startingWord = startingWord[1:6]
    totScore = 0
    count = 0
    for ans in metaLines:
        ans = ans[1:6]
        score = 7
        for attempt in range(1,7):
            if attempt == 1:
                guess = startingWord.lower()
                result = getResult(guess,ans)
                shortLines = lines
            else:
                shortLines = modList(guess,result,shortLines)
                guess = (getGuess(attempt,shortLines))
                result = getResult(guess,ans)

            if result == "GGGGG":
                score = attempt
                break
        totScore += score
        if timer == 0:
            timer = 100
            print("...".format(bestWord))
        else:
            timer -= 1

            
    totScore /= len(metaLines)
    if totScore < bestScore:
        bestScore = totScore
        bestWord = startingWord
    print("Best Word:  {}",format(bestWord))
    print("Best Score: {}",format(bestScore))



















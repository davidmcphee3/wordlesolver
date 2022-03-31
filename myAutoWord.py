#---------------------------------------------------------------#
#                       Wordle AutoPilot
#                          version 1.0
#                         David McPhee
#                      written: Feb-2 2022
#---------------------------------------------------------------#
import copy


def getResult(word,ans):
    arr = [0,1,2,3,4]
    result = []
     
    # get green letters
    word1 = list(zip(word,arr))
    ans1 = list(zip(ans,arr))

    remainingAns = copy.deepcopy(ans1)
    remainingWord = copy.deepcopy(word1)

    strResult = ""

    for testPair in word1:
        if testPair in remainingAns:
            letterResult = ("G",testPair[1])
            remainingAns.remove(testPair)
            remainingWord.remove(testPair)
            result.append(letterResult)

    remainingAnsDummy = copy.deepcopy(remainingAns)
    remainingWordDummy = copy.deepcopy(remainingWord)
    for testPair in remainingWordDummy:  
        for testLetter in remainingAns:
            if testPair[0] == testLetter[0]:
                #print(testLetter)
                #print(remainingAns)
                #print("-----")
                letterResult = ("Y",testPair[1])
                remainingAns.remove(testLetter)
                break
            else:
                letterResult = ("B",testPair[1])              
            
        result.append(letterResult)

    # convert result to string
    result.sort(key = lambda x: x[1])
    for pair in result:
        strResult += pair[0]
    
    return strResult



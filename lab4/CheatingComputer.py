###################
# advanced excercise
###################

import random


def readWords(fileName):
    f = open(fileName, 'r+')
    line = f.readline().strip()
    words.append(line)
    while line != "":
        line = f.readline().strip()
        words.append(line)


def chooseWord(level, prev) -> str:

    random.shuffle(words)
    i = 0
    word = words[i]
    if level == 1:
        while len(word) < 11 or word == prev:
            i += 1
            word = words[i]
    if level == 2:
        while len(word) < 6 or len(word) > 9 or word == prev:
            i += 1
            word = words[i]
    else:
        while len(word) > 5 or word == prev:
            i += 1
            word = words[i]
    return word


def chooseWordByLength(length, prev):
    random.shuffle(words)
    i = 0
    word = words[i]
    while len(word) != length or word == prev:
        print(word)
        i += 1
        word = words[i]
    return word


#             _______                           max hang man
#            |       |
#            |       O
#            |      -|-
#            |     _/ \_
#            |
#            |_____________


def displayMan(fails):
    fails = fails-2
    print(" _______" if fails > -2 else "")
    print("|        "+("|" if fails > -1 else ""))
    print("|        "+("O" if fails > 0 else " "))

    print("|      "+("-" if fails > 2 else " ")+("/" if fails >
          1 else " ")+("-" if fails > 3 else " "))

    print("|     "+("_" if fails > 6 else " ")+("/" if fails > 4 else " ") +
          ("\\" if fails > 5 else " ")+("_" if fails > 7 else " "))

    print("|")
    print("|_____________")


def displayProgress(correctLettersGuessed, actaulWord):
    shown = ""
    for i in range(len(actaulWord)):
        if actaulWord[i] in correctLettersGuessed:
            shown += actaulWord[i]+" "
        else:
            shown += "_ "
    print(shown)

    pass


def checkWin() -> bool:
    for l in chosenWord:
        if l not in correctLetters:
            return False
    return True


def guess(w):
    global tries
    global chosenWord
    tries += 1
    if w in chosenWord:
        if choice == True:
            chosenWord = chooseWordByLength(len(chosenWord), chosenWord)
        else:
            chosenWord = chooseWord(len(chosenWord), chosenWord)

    return False


###################################

# no change required on replays

words = []
readWords("EnglishWords.txt")
###################################

print()
print("rules: ")
print("if just a letter entered as guess then letters may fill the underscoring eg.we have _ _ _ _ _,")
print("a correct letter guess say like 'e' will result in _ e _ _ _ ")
print("if a word is guessed then the player either wins or does not, no letters are added to the")
print("underscoring of the player's progression")

print()

# Game loop
playAgain = True
while playAgain:
    correctLetters = []
    level = 0

    choice = True if str(input(
        "type `yes` if you would like to choose the length of your word and `no` if you would like to enter a level instead")).lower() else False

    if choice == False:
        validLevel = False
        # definetly no more exception handling, takes a while to type :)
        while validLevel == False:
            try:
                level = int(input("enter the level number: "))
                validLevel = True if level > 0 and level < 4 else False
                if not (level > 0 and level < 4):
                    print("enter a integer between 1 and 3 inclusive!")
            except:
                print("enter a integer!")

        chosenWord = chooseWord(level, " ")
    else:
        message = "enter the length of the word: "

        chosenWord = chooseWordByLength(int(input(message)), " ")
    tries = 0
    displayMan(tries)
    displayProgress(correctLetters, chosenWord)

    win = False
    print(chosenWord)
    while win == False and tries < 10:

        user = str(input("enter your guess (a letter only) : "))
        while len(user) != 1:
            user = str(input("enter your guess (a letter only) : "))

       ###############################################################
       # 'guess' function altered to have the cheating computer code
       ###############################################################

        win = guess(user)
        if not win:
            win = checkWin()
        if not win:
            displayMan(tries)
            displayProgress(correctLetters, chosenWord)
        print(chosenWord)

    print("The correct word was: "+chosenWord)
    if win:
        print("Guesses: "+tries)
        print("you win!!!!!!!!!")

    else:
        print("you looooooseee :(")

    playAgain = True if str(
        input("type `yes` if you would like to play again: ")).lower() == "yes" else False

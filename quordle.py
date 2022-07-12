from string import ascii_uppercase as uppers, ascii_lowercase as lowers
from random import choice

def word_score(word):#returns the frequency score of a word, larger is better
    ret = 1
    for letter in set(word):
        ret *= dist[letter]
    return ret

def word_chal(word,guess,color_score):#returns the score of a guess based on previous guesses and results
    if word in hits:
        return 0
    best_ret = 0
    ret = ""
    for pos in range(4):
        temp_ret = 2
        for letter in range(5):
            if color_score[pos][letter] == 'G' and word[letter] == guess[letter]:
                temp_ret = temp_ret**5
            if color_score[pos][letter] == 'G' and word[letter] != guess[letter]:
                temp_ret = 0
                break
            if color_score[pos][letter] == 'Y' and guess[letter] in word and guess[letter] != word[letter]:
                temp_ret = temp_ret**3
            if color_score[pos][letter] == 'Y' and guess[letter] == word[letter]:
                temp_ret = 0
                break
            if color_score[pos][letter] == 'Y' and guess[letter] not in word:
                temp_ret = 0
                break
            if color_score[pos][letter] == 'B' and word[letter] in remaining[pos]:
                temp_ret = temp_ret**1.01
            if color_score[pos][letter] == 'B' and word[letter] in remaining[pos]:
                temp_ret = 0
                break
            if color_score[pos][letter] == 'B' and word[letter] == guess[letter]:
                temp_ret = 0
                break
        if temp_ret > best_ret:
            ret = word
            best_ret = temp_ret
    return best_ret
            
        

def best_guess(guess,color_score):#return the best possible word choice
    rem = []
    best = 0
    for pos in range(4):#position
        for y in range(5):#letter
            if color_score[pos][y] == 'G':#you know the letter
                remaining[pos][y] = [guess[y]]
            elif color_score[pos][y] == 'Y' and guess[y] not in present[pos]:#the letter is there but not in this position
                present[pos].append(guess[y])
                if guess[y] in remaining[pos][y]:
                    remaining[pos][y].remove(guess[y])
            elif color_score[pos][y] == 'B':#the letter is not in the word at that position or any position after
                if guess.count(guess[y]) == 1:
                    for z in range(5):
                        if guess[y] in remaining[pos][z]:
                            remaining[pos][z].remove(guess[y])
                else:
                    for z in range(y,5):
                        if guess[y] in remaining[pos][z]:
                            remaining[pos][z].remove(guess[y])
    for word in flw:#eliminate words that can't be any of the choices
        flags = [True,True,True,True]
        for pos in range(4):
            if len(present[pos]) > 0 and len(set(present[pos]).intersection(set([z for z in word]))) == 0:
                flags[pos] = False
            for letter in range(5):
                if word[letter] not in remaining[pos][letter]:
                    flags[pos] = False
        if flags.count(True) >= best and flags.count(True) > 0:
            best = flags.count(True)
            rem.append(word)
    best = 0
    ret = ''
    keepers = []
    for word in rem:
        temp_score = 1
        for items in stored:
            temp_score *= word_chal(word,items[0],items[1])#find the overall score for the words that are possible
        if temp_score > best:
            best = temp_score
            keepers = [word]
        elif temp_score == best:
            keepers.append(word)
    for store in stored:#delete already used words
        if store[0] in keepers:
            keepers.remove(store[0])
    best = 0
    for word in keepers:#break ties by using letter frequency
        if word_score(word) > best:
            best = word_score(word)
            ret = word
    return word
    
            
            
remaining = [[[x for x in lowers],[x for x in lowers],[x for x in lowers],[x for x in lowers],[x for x in lowers]],
             [[x for x in lowers],[x for x in lowers],[x for x in lowers],[x for x in lowers],[x for x in lowers]],
             [[x for x in lowers],[x for x in lowers],[x for x in lowers],[x for x in lowers],[x for x in lowers]],
             [[x for x in lowers],[x for x in lowers],[x for x in lowers],[x for x in lowers],[x for x in lowers]]]
present = [[],[],[],[]]
flw = []

dist = {}#frequency distribution in 5-letter words

for x in lowers:
    dist[x] = 0        

with open("words2.txt","r") as f:
    for row in f:
        for letter in row[0:5]:
            dist[letter] += 1
        flw.append(row[0:5])

estimate = 4000**5
initials = []
hits = ['','','','']#store correct answers

for c in flw:
    if word_score(c) > estimate:
        initials.append(c)#select starting guesses that have high frequency scores

guess = choice(initials)
print("Initial Guess: "+guess)
if input("Do you want a different guess? (y/n): ").lower() == 'y':
    guess = input("What would you like to guess: ")

stored = []
loc = ['Top Left','Top Right','Bottom Left','Bottom Right']
for turns in range(8):
    keepers = []
    colors = [[],[],[],[]]
    for x in range(4):
        if hits[x] == '':
            colors[x] = input("Colors from "+loc[x]+" (G for green, Y for yellow, B for black): ")
        else:
            colors[x] = 'BBBBB'

        if colors[x] == 'GGGGG':#the word has been found
            remaining[x] = [[],[],[],[],[]]
            hits[x] = guess
    stored.append([guess,colors])
    guess = best_guess(guess,colors)
    print("Suggested Guess: "+guess)
    if input("Do you want a different guess? (y/n): ").lower() == 'y':
        guess = input("What would you like to guess: ")

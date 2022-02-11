import nltk
nltk.download('words')
from nltk.corpus import words
import string
import json

class State: 
    def __init__(self):
        self.initializeWordList()
        self.initializeWordFrequencyCounts()
        self.letters_in_word = {} #{<letter>: <possible idxs [0-4]>, ... } 
        self.letters_not_in_word = {}

    def initializeWordList(self):
        word_list = words.words()
        self.possible_words = []
        for word in word_list: 
            if len(word) == 5:
                self.possible_words.append(word)
    
    def initializeWordFrequencyCounts(self):
        wordFrequencyFile = 'word_frequency.json'
        try:
            f = open(wordFrequencyFile)
            wordFrequency = json.load(f)
            self.word_frequencies = wordFrequency
        except: 
            print('failed to open jsons ... make sure {wordFrequencyFile} exists in dir')
            exit(1)

    # feedback is list of form
    # ['a,0', 'b,1', 'c,2', 'd,1', 'e,1']
    def parseLetterHints(self, letter_hints):
        for i in range (0, len(letter_hints)):
            letter_hint = letter_hints[i]
            letter_hint_split = letter_hint.split(',')
            c = letter_hint_split[0]
            hint = int(letter_hint_split[1])
            if hint == 0:
                self.letters_not_in_word[c] = True
            elif hint == 1:
                if c in self.letters_in_word:
                    self.letters_in_word[c].remove(i)
                else:
                    new_poss_idxs = [0, 1, 2, 3, 4]
                    new_poss_idxs.remove(i)
                    self.letters_in_word[c] = new_poss_idxs
            else:
                self.letters_in_word[c] = [i]

    def printState(self):
        print(f"letters in word: {self.letters_in_word}")
        print(f"letters not in word: {self.letters_not_in_word}")

    def wordIsEligible(self, word):
        word_arr = list(word)
        for i in range(0, len(word_arr)):
            c = word_arr[i]
            if c in self.letters_not_in_word:
                #print(f'{word} is not eligible - {c} not in word')
                return False
            elif c in self.letters_in_word and i not in self.letters_in_word[c]:
                #print(f'{word} is not eligible - {c} in word, wrong place')
                return False
        
        for letter, idxs in self.letters_in_word.items():
            # word has to have the letter at one of those idxes
            is_letter_at_possible_idx = False
            for idx in idxs: 
                if word_arr[idx] == letter:
                    is_letter_at_possible_idx = True
            if not is_letter_at_possible_idx:
                return False
        return True

    def updatePossibleWords(self):
        remaining_possibles = []
        for word in self.possible_words:
            if self.wordIsEligible(word):
                remaining_possibles.append(word)
        self.possible_words = remaining_possibles
        self.possible_words.sort(reverse=True, key=self.getSortOrder)
        return self.possible_words
    
    def getSortOrder(self, word):
        if word in self.word_frequencies: 
            return self.word_frequencies[word]
        else:
            return 0


# <letter>,<letter hint> 
# letter is [a-z]
# letter hint is 
#   0: not in word
#   1: in word
#   2: in index
def takeGuessFeedback(n_letters): 
    letter_inputs = []
    for i in range(0,n_letters):
        letter_inputs.append(input())
    return letter_inputs


game_state = State()
for i in range(0, 5):
    print(f"Input the feedback for your guess({i+1}) on the next 5 lines each letter of format (a,1):")
    raw_feedback = takeGuessFeedback(5)
    game_state.parseLetterHints(raw_feedback)
    game_state.updatePossibleWords()
    print(game_state.possible_words)
    print("\n")

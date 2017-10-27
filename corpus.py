import os 
import csv 

#REFACTOR check if memory loaded multiple times  
# source lexicon: http://www.wordgamedictionary.com/twl06/download/twl06.txt = the FreeScrabbleDictionary_twl06.txt, used in North American tournaments
def load_corpus():
    corpus = []
    with open(os.path.join(os.path.dirname( __file__ ), 'static', 'data', 'FreeScrabbleDictionary_twl06.txt'), newline = '') as raw_corpus:
        for word in csv.reader(raw_corpus):
            cleaned_word = ''.join(word).upper()
            if len(cleaned_word) >= get_min_word_length(): #this excludes 'A' and 'I'...for now...TBD
                corpus.extend([cleaned_word])
    return corpus
    
def get_min_word_length():
    return 2

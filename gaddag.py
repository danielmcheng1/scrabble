import os 
import _pickle as pickle
import string 
import gaddag_node 
import corpus 

# original implementation: 1820 megabytes for loading official Scrabbl dictionary into gaddag (178 k words)
# compressed suffixes for a given word and added eow letter sets: 854 mb!

# use gaddag module to hold global variable pointing to corpus 
SCRABBLE_CORPUS = corpus.load_corpus()
SCRABBLE_CORPUS_NAME = "TWL06 Official Scrabble Dictionary"

# writing and reading gaddag (precompute/preload ahead of time) 
def write_gaddag_full():
    output_file = open(os.path.join(os.path.dirname( __file__ ), 'static', 'data', 'gaddag_full.txt'), 'wb')
    scrabble_gaddag = gaddag(SCRABBLE_CORPUS, output_file)
    output_file.close()
    return scrabble_gaddag 

# pass in corpus in case we need to create the gaddag
def read_gaddag_full():
    gaddag_filename = os.path.join(os.path.dirname(__file__), 'static', 'data', 'gaddag_full.txt')
    if os.path.isfile(gaddag_filename):
        input_file = open(gaddag_filename, 'rb') 
        return pickle.load(input_file)
    else:
        return write_gaddag_full()
    
    
   
# the hook represents where the prefix ends (up to and including the intersection tile) 
# so this is the point at which we flip from prefix building to suffix building
GADDAG_HOOK = "@"             
class gaddag:
    def __init__(self, corpus, output_file = None):
        self.start_node = gaddag_node.gaddag_node()
        self.make_gaddag(corpus, output_file)
        
    def make_gaddag(self, corpus, output_file = None):
        for word in corpus:
            self.add_word(word)
        if output_file is not None:
            pickle.dump(self, output_file)
    def add_word(self, word):
        n = len(word)
        next_node = self.start_node
        for i in range(n - 1, 1, -1):
            next_node = next_node.add_edge(word[i])
        next_node = next_node.add_eow(word[1], word[0])
        #no need to add hook since no suffix exists
        next_node = self.start_node  
        
        for i in range(n - 2, -1, -1):
            next_node = next_node.add_edge(word[i])
        next_node = next_node.add_eow(GADDAG_HOOK, word[n-1])  
        
        for i in range(n - 3, -1, -1):
            forced_node = next_node
            next_node = self.start_node
            rev_prefix = word[i::-1]
            for letter in rev_prefix:
                next_node = next_node.add_edge(letter)
            next_node = next_node.add_edge(GADDAG_HOOK)
            next_node.force_edge(word[i+1], forced_node)   
            
    #for printing entire gaddag
    def print_gaddag(self):
        print("\n")
        self.start_node.print_node("", "")
    
    #for printing the paths for a list of consecutive letters (typically used to trace a prefix IN REVERSE)
    def print_select_gaddag_paths(self, start_letters):
        print("\n")
        start_path = ""
        start_indent = ""
        curr_node = self.start_node
        #we will try to find this full word in the Gaddag, which will appear as the reversed full prefix
        while len(start_letters):
            letter = start_letters.pop() #this traces the letters in reverse
            if letter in curr_node.edges.keys():
                if curr_node.eow_set:
                    print (start_path + str(curr_node.eow_set))
                start_path = start_path + letter + "-->"
                start_indent = start_indent + gaddag_node.GADDAG_PRINT_INDENT
                curr_node = curr_node.edges[letter]
            elif not curr_node.edges or curr_node.eow_set: 
                if letter not in curr_node.eow_set:
                    print("Not in Gaddag")
                print (start_path + str(curr_node.eow_set))
                return
            else:
                print("Not in Gaddag")
                print(start_path + str(curr_node.eow_set))
                return
        curr_node.print_node(start_indent, start_path)

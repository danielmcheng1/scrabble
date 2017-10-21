
#Gaddag naive implementation: 1820 megabytes for scrabble_gaddag
#partially compressed suffixes for a given word and eow letter sets: 854 mb!
#Execution time: 20-30 seconds for initial load
    
#global vars solely for printing (not for identifying)
GADDAG_PRINT_EOW = "."
GADDAG_PRINT_INDENT = "    "  
GADDAG_PRINT_ARROW = "-->"
class gaddag_node:
    def __init__(self):
        self.edges = dict()
        self.eow_set = set() 
        #a set tells us that we've reached the end of a word
        #we can use a set because any path leading to it is a word for any letter in that set
        #and any subsequent forced states share that same prefix (i.e. they are iterations of the same word)
      
    def add_eow(self, next_letter, eow_letter):
        if next_letter not in self.edges.keys():
            self.edges[next_letter] = gaddag_node()
        next_node = self.edges[next_letter]
        next_node.eow_set.add(eow_letter)
        return next_node
    
    def add_edge(self, next_letter):
        if next_letter not in self.edges.keys():
            self.edges[next_letter] = gaddag_node()
        return self.edges[next_letter]
    #If key is in the dictionary, return its value. 
    #If not, insert key with a value of default and return default. default defaults to None.
            #setdefault(key[, default])

    def force_edge(self, next_letter, forced_node):
        if next_letter in self.edges.keys() and not self.edges[next_letter] == forced_node:
            raise ValueError("Attempting to force an edge but an edge already exists to a different node for " + \
                             str(next_letter) + " to " + str(self.edges[next_letter].eow_set))
        self.edges[next_letter] = forced_node
        return self.edges[next_letter]
    
    def print_node(self, indent, path):
        node_edge_num = 0
        #either we've reached the end of a chain of nodes, 
        #or we can still continue on but we've reached an intermeidate eow set 
        if not self.edges or self.eow_set: 
            print (path + str(self.eow_set))
        for k in self.edges.keys():
            node_edge_num += 1
            if node_edge_num == 1:
                path = path + k + GADDAG_PRINT_ARROW
            else:
                path = indent + k + GADDAG_PRINT_ARROW
            self.edges[k].print_node(indent + GADDAG_PRINT_INDENT, path)
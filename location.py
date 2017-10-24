class Location:
    def __init__(self, row, col):
        self.row = row 
        self.col = col 
    
    def get_row(self):
        return self.row 
    
    def get_col(self):
        return self.col 
    
    def get_tuple(self):
        return (self.row, self.col) 
        
    def offset(self, row_delta, col_delta):
        return Location(self.row + row_delta, self.col + col_delta)
        
    def serialize(self):
        return {"row": self.row,  "col": self.col}
        
    def __str__(self):
        return "({0}, {1})".format(self.row, self.col)
    
    def __repr__(self):
        return "({0}, {1})".format(self.row, self.col)
    
    def __eq__(self, other):
        return self.get_row() == other.get_row() and self.get_col() == other.get_col() 
    
    def __ne__(self, other):
        return not self.__eq__(other)
        
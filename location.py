class Location:
    def __init__(self, row, col):
        self.row = row 
        self.col = col 
    
    def get_row(self):
        return self.row 
    
    def get_col(self):
        return self.col 
    
    def serialize(self):
        return {"row": self.row,  "col": self.col}
        
    def __str__(self):
        return "({0}, {1})".format(self.row, self.col)
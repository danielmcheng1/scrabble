
#TBD player name, type, or ID?    
class tile:
    def __init__(self, letter, points, player, location):
        self.letter = letter
        self.player = player
        self.points = points
        self.location = location 
        
    def serialize(self):
        return {'letter': self.letter, 'points': self.points, 'player': self.player.serialize, 'location': self.location.serialize}

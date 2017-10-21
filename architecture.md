## APIs
Front End 
    only ever sends a move--board object is irrelevat

Wrapper    
    pivot into Javascript form 
        need board, player racks, game info (incl. last move) 
    object to JSON (extra step to Javascript?) 
    JSON to object 
    
Game Play 
    start game 
    make_move of ENUM 
        exchange tiles 
        place tiles 
        pass
        
    last_move method caches last move 
        errors handled as well--so 
            e.g. computer exchanges/passes, or 
            e.g. human placed illegal word turns/score all incremented 
    
    generate_move vs 
    make_move(player)--access parent class 
        uses board instance within game play 
        
    CONTAINS 
        board, score dict, freq dict, corpus, bag 
  
  
Board 
    primarily object store 
 
Generate move 
    includes find crosswords, etc. 
    Find feasible moves
        scrabble tiles in rack (can be filtered down)
        scrabble tiles on board
        GADDAG 
        BOARD 
    Find optimal moves 
        scrabble tiles in rack (can be filtered down)
        scrabble tiles on board 
        GADDAG

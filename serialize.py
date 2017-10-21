
#wrapper to replace scrabble_game.game_play method so that we can interface with flask/web app            
#change to be last move object separate....
def wrapper_play_next_move(data):
    print("Received data in scrabble_apprentice: {0}".format(str(data)))
    #initialize board 
    if data.get("scrabble_game_play", {}) == {}:
        (scrabble_score_dict, scrabble_freq_dict, scrabble_bag, scrabble_corpus) = load_all()
        scrabble_board = board(scrabble_bag, scrabble_score_dict, scrabble_corpus)
            
        human_player = scrabble_player("Human", IS_HUMAN, scrabble_board)  
        computer_player = scrabble_player("Computer", IS_COMPUTER, scrabble_board)  
        scrabble_game_play = game_play(scrabble_board, human_player, computer_player) 
        last_move_to_send = {"action": "Game Started", "player": "", "detail": ""}
        return wrapper_save_game_play(scrabble_game_play, last_move_to_send)
    
    
    #otherwise read in the latest data and make the next move
    print("making human move")    
    scrabble_game_play = data["scrabble_game_play"]
    human_player = scrabble_game_play.play_order[0]
    computer_player = scrabble_game_play.play_order[1]
    scrabble_board = scrabble_game_play.board 
    last_move_to_send = {}
    
    #in case no data is passed through (e.g. relogging back into a session) 
    if data["scrabble_game_play_wrapper"]["last_move"] == {}:
        last_move_to_send = {"action": "Continuing Game from Previous Session", "player": "", "detail": ""}
        return wrapper_save_game_play(scrabble_game_play, last_move_to_send)
    
    #make human move    
    if data["scrabble_game_play_wrapper"]["last_move"]["action"] == "Try Passing":
        human_player.words_played.append({"word": list("PASSED"), "score": 0})
        last_move_to_send["player"] = "Human"
        last_move_to_send["action"] = "Passed"
        last_move_to_send["detail"] = ""           
    elif data["scrabble_game_play_wrapper"]["last_move"]["action"] == "Try Exchanging Tiles":
        tiles_to_exchange = data["scrabble_game_play_wrapper"]["last_move"]["detail"]
        try:
            scrabble_game_play.exchange_tiles_during_turn(human_player, tiles_to_exchange) 
            human_player.words_played.append({"word": list("EXCHANGED"), "score": 0})
            last_move_to_send["player"] = "Human"
            last_move_to_send["action"] = "Exchanged Tiles"
            last_move_to_send["detail"] = ""
        except ValueError as e:
            log_illegal_move(last_move_to_send, e)
    elif data["scrabble_game_play_wrapper"]["last_move"]["action"] == "Try Placing Tiles":
        tiles_to_place = data["scrabble_game_play_wrapper"]["last_move"]["detail"]
        try: 
            full_placement = scrabble_board.convert_placed_tiles_to_full_placement(tiles_to_place)
            score = scrabble_board.make_human_move(full_placement["start_row"], full_placement["start_col"], full_placement["direction"], full_placement["word"], human_player)
            last_move_to_send["player"] = "Human"
            last_move_to_send["action"] = "Placed Tiles"
            last_move_to_send["detail"] = full_placement["word"] 
            wrapper_end_turn(human_player, full_placement["word"], score, scrabble_game_play)
        except ValueError as e:   
            log_illegal_move(last_move_to_send, e)
            
    print("last move:", last_move_to_send["action"]);
    if last_move_to_send["action"] != "Made Illegal Move":
        #increment for human passing 
        increment_turns_passed(scrabble_game_play, last_move_to_send)
        print("num turns passed: {0}".format(scrabble_game_play.num_turns_passed))
           
        print("Game has ended: {0}, game end reason: {1}".format(scrabble_game_play.game_has_ended(), scrabble_game_play.game_end_reason()))
        if scrabble_game_play.game_has_ended():
            return wrapper_save_game_play(scrabble_game_play, last_move_to_send)
            
        #make computer move 
        print("Computer move")
        (score, word) = scrabble_game_play.board.make_computer_move(computer_player)     
        #if the computer is unable to find a move, exchange tiles
        print("score: {0}, word {1}".format(score, str(word)))
        if word == []:
            try: 
                scrabble_game_play.exchange_tiles_during_turn_capped(computer_player, computer_player.rack)
                last_move_to_send["action"] = "Exchanged Tiles"
                human_player.words_played.append({"word": list("EXCHANGED"), "score": 0})
            except ValueError as e:
                last_move_to_send["action"] = "Passed"
                human_player.words_played.append({"word": list("PASSED"), "score": 0})
            last_move_to_send["player"] = "Computer"
            last_move_to_send["detail"] = "" #could return tiles exchanged instead
        else: 
            last_move_to_send["player"] = "Computer"
            last_move_to_send["action"] = "Placed Tiles" 
            last_move_to_send["detail"] = word
            wrapper_end_turn(computer_player, word, score, scrabble_game_play)
        increment_turns_passed(scrabble_game_play, last_move_to_send)
    return wrapper_save_game_play(scrabble_game_play, last_move_to_send)
    
def wrapper_save_game_play(scrabble_game_play, last_move_to_send):   
    print("wrapping") 
    human_player = scrabble_game_play.play_order[0]
    computer_player = scrabble_game_play.play_order[1]
    scrabble_board = scrabble_game_play.board
    scrabble_score_dict = scrabble_board.scrabble_score_dict
    
    scrabble_game_play_wrapper = {"board": [[map_cell_to_bonus_view(scrabble_board.board[row][col]) for col in range(MAX_COL)] for row in range(MAX_ROW)], \
                              "tiles": [[map_cell_to_tile_view(scrabble_board.board[row][col], map_cell_to_player_view(row, col, scrabble_board), scrabble_score_dict) for col in range(MAX_COL)] for row in range(MAX_ROW)], \
                              "rackHuman": map_rack_to_tile_view(human_player.rack, "Human", scrabble_score_dict),   \
                              "rackComputer": map_rack_to_tile_view(computer_player.rack, "Computer", scrabble_score_dict), \
                              "gameInfo": {"scoreHuman": human_player.running_score, "scoreComputer": computer_player.running_score,
                                           "wordsPlayedHuman": human_player.words_played, "wordsPlayedComputer": computer_player.words_played,
                                           "tilesLeft": len(scrabble_board.bag),
                                           "gameEndReason": scrabble_game_play.game_end_reason()}, \
                              "lastMove": last_move_to_send
                              }
                              
    return {"scrabble_game_play_wrapper": scrabble_game_play_wrapper, "scrabble_game_play": scrabble_game_play}

def wrapper_end_turn(player, word, score, game_play):
    player.words_played.append({"word": word, "score": score})
    player.running_score += score   
    game_play.draw_tiles_end_of_turn(player, RACK_MAX_NUM_TILES - len(player.rack)) 
    
def increment_turns_passed(scrabble_game_play, move):
    if move["action"] == "Passed":
        scrabble_game_play.num_turns_passed += 1
    else:
        scrabble_game_play.num_turns_passed = 0 
        
def log_illegal_move(last_move_to_send, e):
    last_move_to_send["player"] = "Human"
    last_move_to_send["action"] = "Made Illegal Move" 
    last_move_to_send["detail"] = "".join(e.args)
    
def map_cell_to_bonus_view(cell):
    if cell == TRIPLE_LETTER:
        return 'Triple Letter'
    if cell == TRIPLE_WORD:
        return 'Triple Word'
    if cell == DOUBLE_LETTER:
        return 'Double Letter'
    if cell == DOUBLE_WORD:
        return 'Double Word'
    if cell == NO_BONUS:
        return ''
    #TBD have to see if bonusess get replaced by letters 
    #print('WARNING: returning blank for {0}'.format(cell))
    return ''
    
def map_cell_to_tile_view(cell, player_type, scrabble_score_dict):
    #TBD flip to the is_scrabble_tile method? 
    #TBD player type vs. player vs. player name
    #cell is actually a tile...
    if cell.isalpha():
        return tile(cell, player_type, scrabble_score_dict).get_tile()
    return ''
    
def map_cell_to_player_view(row, col, scrabble_board):
    return scrabble_board.board_to_player[row][col]

def map_rack_to_tile_view(rack, player_type, scrabble_score_dict):
    return [tile(letter, player_type, scrabble_score_dict).get_tile() for letter in rack]
        
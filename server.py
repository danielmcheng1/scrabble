
import sys 
import flask 
import flask_login 

import game_controller 
import server_user_database 

app = flask.Flask(__name__)
app.secret_key = 'temporary secret string'
login_manager = flask_login.LoginManager() 
login_manager.init_app(app)


ALL_SESSIONS = {}
@app.route('/loadNewGame',methods=['POST'])
def load_new_game():
    print('Logged in as: ' + flask_login.current_user.id)
    session_id = flask_login.current_user.id
    game = game_controller.GameController()
    print('Returning')
    
    ALL_SESSIONS[session_id] = game
    return flask.jsonify(game.serialize())


@app.route('/processMove',methods=['POST'])
def process_move():
    print('---------------- Logged in as: ' + flask_login.current_user.id)
    session_id = flask_login.current_user.id
    
    user_json = flask.request.json if flask.request.json is not None else {}
    print('-----------------Received json:\n {0}'.format(user_json), file=sys.stderr)
    
    
    game = ALL_SESSIONS[session_id]
    game.process_human_move(user_json["action"], game.front_end_json_to_tiles(user_json))
    
    print('--------------- SENDING JSON BACK')
    game.print_serialize()
    return flask.jsonify(game.serialize())
    # session_data = SCRABBLE_APPRENTICE_DATA.setdefault(session_id, {})
@app.route('/moveDoneHuman2',methods=['POST'])    
def process_human_move():
    print('Logged in as: ' + flask_login.current_user.id)
    
    session_id = flask_login.current_user.id
    user_data = flask.request.json if flask.request.json is not None else {}
    print('Received json {0}'.format(user_data), file=sys.stderr)
    
    #TBD temporary override--if restarting, we have to force a reset  
    if user_data.get("Restart Game") == "Y":
        SCRABBLE_APPRENTICE_DATA[session_id] = {}   
    #pull data for this session, or create a new session id key
    session_data = SCRABBLE_APPRENTICE_DATA.setdefault(session_id, {})
    
    #reset the front-end wrapper and save the last move for the back end
    session_data["scrabble_game_play_wrapper"] = {} 
    
    #save the last move 
    session_data["scrabble_game_play_wrapper"]["last_move"] = user_data.get("last_move", {})
    
    #now process on the back end
    SCRABBLE_APPRENTICE_DATA[session_id] = scrabble_apprentice.wrapper_play_next_move(session_data)
    scrabble_game_play_wrapper = SCRABBLE_APPRENTICE_DATA[session_id]["scrabble_game_play_wrapper"]
  
    print("Sending back:\n" + str(scrabble_game_play_wrapper))
    return flask.jsonify(scrabble_game_play_wrapper)

# no password -- using login simply to save and cache sessions
class User(flask_login.UserMixin): 
    pass 
@login_manager.user_loader 
def user_loader(username):
    if username not in server_user_database.users:
        return 
    user = User() 
    user.id = username 
    return user

@login_manager.request_loader 
def request_loader(request):
    username = request.form.get('username')
    if username not in server_user_database.users:
        return 
    user = User()
    user.id = username 
    
    user.is_authenticated = request.form['password'] == server_user_database.users[username]['password']
    return user 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html') 
        
    username = flask.request.form['username']
    password = ''
    if username == '':
        return flask.render_template("login.html", login_failure_message = "Please create a username to begin play")
    if username not in server_user_database.users:
        server_user_database.users[username] = {'password': password}
        user = User() 
        user.id = username 
        flask_login.login_user(user) 
        return flask.redirect(flask.url_for('play_game'))
        
    if password == server_user_database.users[username]['password']:
        user = User() 
        user.id = username 
        flask_login.login_user(user) 
        return flask.redirect(flask.url_for('play_game'))
   
    return flask.render_template("login.html", login_failure_message = "Please create a username to begin play")

@login_manager.unauthorized_handler 
def unauthorized_handler():
    return flask.render_template("login.html", login_failure_message = "Please create a username to begin play")
        
@app.route('/game',methods=['GET','POST'])
@flask_login.login_required
def play_game():
    print('Logged in as: ' + flask_login.current_user.id)
    return flask.render_template('game.html')

  
if __name__ == '__main__':
    # Production 
    app.run(host='0.0.0.0', port=8000)
    # Dev 
    # app.run()
    

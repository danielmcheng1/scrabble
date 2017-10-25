
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
@app.route('/loadNewGame',methods=['GET', 'POST'])
def load_new_game():
    print('Loading new game for: ' + flask_login.current_user.id)
    session_id = flask_login.current_user.id
    game = game_controller.GameController()
    
    ALL_SESSIONS[session_id] = game
    return flask.jsonify(game.serialize())


@app.route('/processMove',methods=['GET', 'POST'])
def process_move():
    print('Processing move for: ' + flask_login.current_user.id)
    session_id = flask_login.current_user.id
    
    user_json = flask.request.json if flask.request.json is not None else {}
    print('Received json:\n {0}'.format(user_json), file=sys.stderr)
    
    game = ALL_SESSIONS[session_id]
    game.process_human_move(user_json["action"], game.front_end_json_to_tiles(user_json))
    
    print('Sending back update game data')
    game.print_serialize()
    return flask.jsonify(game.serialize())
    

# no password -- we areusing login simply to save and cache sessions
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
    print('Loading game page as: ' + flask_login.current_user.id)
    return flask.render_template('game.html')

  
if __name__ == '__main__':
    # Production 
    app.run(host='0.0.0.0', port=8000)
    # Dev 
    # app.run()
    

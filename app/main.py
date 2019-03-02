import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    print(data['board']['width'])
    color = "#736CCB",
	#headType: "beluga",
    #tailType: "curled"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.

    """
    #print("DUMPING")
    #print(json.dumps(data))
    #print("JUST ME")
    #print(data['you'])
    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)

    me = data['you']

    width = data['board']['width']

    #print(me['body'][0])


    board = [[0 for i in range(width)] for j in range(width)]

    #grabs our body coordinates
    for item in me['body']:
        print("X = " + str(item['x']) + " Y = " +str(item['y']))
        board[item['x']][item['y']] = 1

    #print (board)
    x = me['body'][0]['x']
    y = me['body'][0]['y']
    print(me['health'])

    if(y+1 < width and board[x][y+1] == 0):
        print("chose down" + str(board[x][y+1]))
        direction = 'down'
    elif( x+1 < width and board[x+1][y] == 0 ):
        print("chose right" + str(board[x+1][y]))
        print("X+1 = " + str(x+1))
        direction = 'right'
    elif(x-1 > 0 and board[x-1][y] == 0 ):
        print("chose left" + str(board[x-1][y]))
        direction = 'left'
    else:
        print("went up")
        direction = 'up'


    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    #print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )

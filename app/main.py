import json
import os
import random
import operator
import bottle
import math

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
    color = "#42f4c8"

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
        board[item['x']][item['y']] = 'm'
        # square with self is m

    snakes = data['board']['snakes']
    for snake in snakes:
        counter = 0;
        for others in snake['body']:

            if(counter == 0 and board[others['x']][others['y']] != 'm'):
                board[others['x']][others['y']] = 'o'
                #make do stuff
            else:
                board[others['x']][others['y']] = 'o'
            counter += 1;
            # square with other snake is o

    #print(snakes)
    for food in data['board']['food']:
        board[food['x']][food['y']] = 'f'
        # square with food is f

    #print (board)
    x = me['body'][0]['x']
    y = me['body'][0]['y']
    print(me['health'])

    #0 = left, 1 = up, 2 = right, 3 = down
    priorityDirections = {
        "left": 0,
        "right": 0,
        "up": 0,
        "down": 0
    }

    distFoodLeft = []
    distFoodRight = []
    distFoodUp = []
    distFoodDown = []

    if(y+1 < width and board[x][y+1] != 'm' and board[x][y+1] != 'o' ):
        print("chose down" + str(board[x][y+1]))
        priorityDirections["down"] += 1

        if(data['you']['health'] < 50):
            for food in data['board']['food']:
                dist = math.sqrt( (x - food['x'])**2 + (y+1 - food['y'])**2 )
                distFoodDown.append(dist)

            priorityDirections["down"] += 100 - min(distFoodDown)
        #possibleDirections.append('down')
    if( x+1 < width and board[x+1][y] != 'm' and board[x+1][y] != 'o'):
        print("chose right" + str(board[x+1][y]))
        print("X+1 = " + str(x+1))
        priorityDirections["right"] += 1
        if(data['you']['health'] < 50):
            for food in data['board']['food']:
                dist = math.sqrt( (x+1 - food['x'])**2 + (y - food['y'])**2 )
                distFoodRight.append(dist)

            priorityDirections["right"] += 100 - min(distFoodRight)
        #possibleDirections.append('right')
    if(x-1 >= 0 and board[x-1][y] != 'm' and board[x-1][y] != 'o'):
        print("chose left" + str(board[x-1][y]))
        #possibleDirections.append('left')
        priorityDirections["left"] += 1
        if(data['you']['health'] < 50):
            for food in data['board']['food']:
                dist = math.sqrt( (x-1 - food['x'])**2 + (y - food['y'])**2 )
                distFoodLeft.append(dist)
            priorityDirections["left"] += 100 - min(distFoodLeft)

    if(y-1 >= 0 and board[x][y-1] != 'm' and board[x][y-1] != 'o'):
        print("went up")
        priorityDirections["up"] += 1
        if(data['you']['health'] < 50):
            for food in data['board']['food']:
                dist = math.sqrt( (x - food['x'])**2 + (y-1 - food['y'])**2 )
                distFoodUp.append(dist)
            #possibleDirections.append('up')

            priorityDirections["up"] += 100 - min(distFoodUp)



    #direction = random.choice(possibleDirections)
    direction = max(priorityDirections.iteritems(), key=operator.itemgetter(1))[0]

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

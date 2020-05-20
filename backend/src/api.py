import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# '''
# @TODO uncomment the following line to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
# '''
#db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods = ['GET'])
def get_drinks():

    drinks_query = Drink.query.all()
    drinks=[drink.short() for drink in drinks_query]

    return jsonify({
    'success': True,
    'drinks': drinks
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods = ['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks_query = Drink.query.all()
    drinks=[drink.long() for drink in drinks_query]
    return jsonify({
    'success': True,
    'drinks': drinks
    })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/create', methods= ['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    #obtain info as json object
    body = request.get_json()
    title = body.get('title')
    recipe = json.dumps(body.get('recipe'))
    #insert key elements needed for drink
    drink = Drink(
    title = title,
    recipe = recipe
    )
    drink.insert()

    return jsonify({
    'success': True,
    'drinks': [drink.long()]
    })

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods= ['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload):
    #obtain info as json object and targeted drink to update
    body = request.json()
    drink = Drink.query.filter(Drink.id==id).one_or_none()

    #abort if no results found
    if not drink:
        abort(404)

    #set new information and update record of target drink
    else:
        drink.title = body.get('title')
        drink.recipe = json.dumps(body.get('recipe'))
        drink.insert()

    return jsonify({
    'success': True,
    'drinks': [drink.long()]
    })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods= ['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload):
    #obtain info as json object and targeted drink to update
    body = request.json()
    drink = Drink.query.filter(Drink.id==id).one_or_none()

    #abort if no results found
    if not drink:
        abort(404)

    #set new information and update record of target drink
    else:
        drink_id = drink.id
        drink.delete()

    return jsonify({
    'success': True,
    'delete': drink_id
    })


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource missing"
                    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def auth_error_message(error):
    print (AuthError)
    return jsonify({
                    "success": False,
                    "description":"Authorization Error"
                    })

if __name__=='__main__':
    app.run(debug=True)

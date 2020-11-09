# authentication.py
# * Rev.1: 2020-09-24 (Thu)
# * Draft: 2020-09-21 (Mon)
#
# This code is from:
#   '깔끔한 파이썬 탄탄한 백엔드', '7장 인증', 송은우 지음, pp.188-200
#   https://github.com/rampart81/python-backend-book/tree/master/chapter7

import bcrypt
import jwt

@app.route( '/sign-up', methods=['POST'] )
def sign_up():
  new_user             = request.json
  new_user['password'] = bcrypt.hashpw(
    new_user['password'].encode('UTF-8'),
    bcrypt.gensalt()
  )
  new_user_id = app.database.execute( text("""
    INSERT INTO users(
      name,
      email,
      profile,
      hashed_password
    ) VALUES (
      :name,
      :email,
      :profile,
      :password
    )
  """), new_user).lastrowid
  new_user_info = get_user( new_user_id )

  return jsonify( new_user_info )

@app.route( '/login', methods=['POST'] )
def login():
  credential = request.json
  email      = credential[ 'email' ]
  password   = credential[ 'password' ]

  row = database.execute( text("""
    SELECT id, hashed_password
    FROM users
    WHERE email = :email
  """), {'email' : email }.fetchone()

  if row and bcrypt.checkpw( password.encode('UTF-8'), row['hashed_password'].encode('UTF-8') ):
    user_id = row['id']
    payload = {
      'user_id' : user_id,
      'exp'     : datetime.utcnow() + timedelta( seconds = 60*60*24 )
    }
    token = jwt.encode( payload, app.config['JWT_SECRET_KEY'], 'HS256' )

    return jsonify({
      'access_token' : token.decode('UTF-8')
    })
  else:
    return '', 401

@run_this_first
def and_then_run_this()
  print( "Running the second method..." )

from functools import wraps

def test_decorator(f):
  @wrap(f)
  def decorated_function( *args, **kwargs ):
    print( "Decorated Function" )
    return f( *args, **kwargs )

  return decorated_function

@test_decorator
def func():
  print( "Calling func function" )

# authentication decorator function, p.194
import jwt

from functools import wraps
from flask     import request, Response

def login_required(f):
  @wraps(f)
  def decorated_function( *args, **kwargs ):
    access_token = request.headers.get( 'Authorization' )
    if access_token is not None:
      try:
        payload = jwt.decode( access_token, current_app.config['JWT_SECRET_KEY', 'HS256']
      except jwt.InvalidTokenError:
        payload = None

      if payload is None:
        return Response( status=401 )

      user_id   = payload[ 'user_id' ]
      g.user_id = user_id
      g.user    = get_user_info( user_id ) if user_id else None
    else:
      return Response( status= 401 )

    return f( *args, **kwargs )
  return decorated_function

# applying authentication decorator, pp.196-197

def insert_tweet( user_tweet ):
  return current_app.database.execute( text("""
    INSERT INTO tweets (
      user_id,
      tweet
    ) VALUES (
      :id,
      :tweet
    )
   """), user_tweet ).rowcount

def insert_follow( user_follow ):
  return current_app.database.execute( text("""
    INSERT INTO users_follow_list (
      user_id,
      follow_user_id
    ) VALUES (
      :id,
      :follow
    )
  """), user_follow ).rowcount

def insert_unfollow( user_unfollow ):
  return current_app.database.execute( text("""
    DELETE FROM users_follow_list
    WHERE user_id = :id
    AND follow_user_id = :unfollow
  """), user_unfollow).rowcount

@app.route('/tweet', methods=['POST'])
@login_required
def tweet():
  user_tweet       = request.json
  user_tweet['id'] = g.user_id
  tweet            = user_tweet[ 'tweet' ]
  
  if len( tweet ) > 300:
    return 'Exceeded the 300 character limit', 400

  insert_tweet( user_tweet )

  return '', 200

@app.route('/follow', methods=['POST'])
@login_required
def follow():
  payload = request.json
  insert_follow( payload )
  return '', 200

@app.route('/unfollow', methods=['POST'])
@login_required
def unfollow():
  payload = request.json
  insert_unfollow( payload )
  return '', 200


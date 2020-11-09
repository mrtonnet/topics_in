# miniter.py
# * Draft: 2020-09-21 (Mon)
#
#  This file is the same as timeline.py.
#  timeline.py is used to emphasize the timeline endpoint's implementation.
#
# Minitor's core functions
#   sign-up
#   log-in
#   tweet
#   follow
#   unfollow
#   timeline
#
# 

from flask import Flask, jsonify, request
from flask.json import JSONEncoder

#-----------------------------
#  Custom class definitions  #
#-----------------------------
# The data structure to store user_id_to_follow is 'set'.
# A set cannot be converted to JSON with the json module
#   while a list can be converted to JSON.
# So write a Custom JSON Encoder to convert a set to a list.

# Flask converts a list to JSON automatically,
#   but a set can't be converted resulting in an error.
class CustomJSONEncoder( JSONEncoder ):
  # if a set is used, convert it to a list
  def default( self, obj ):
    if isinstance( obj, set ):
      return list(obj)

  # else use the default JSONEncoder
    return JSONEncoder.default( self, obj )

#-------------------------------
app          = Flask( __name__ )
app.users    = {} 
app.id_count = 1
app.tweets   = []
app.json_encoder = CustomJSONEncoder  # Overwrite the default json_encoder with the custom JSON encoder

#-------------------------
#  Function definitions  #
#-------------------------
@app.route( '/ping', methods=[ 'GET' ] )
def ping():
  return 'pong'

@app.route( '/sign-up', methods=[ 'POST' ] )
def sign_up():
  new_user                  = request.json
  new_user[ 'id' ]          = app.id_count
  app.users[ app.id_count ] = new_user
  app.id_count              = app.id_count + 1

  return jsonify( new_user )

# An example JSON data or the payload within the request is:
# {
#   "id"   : 1,
#   "tweet" : "My First Tweet"
# }

@app.route( '/tweet', methods=[ 'POST' ] )
def tweet():
  payload = request.json
  user_id = int( payload['id'] )
  tweet   = payload['tweet']

  if user_id not in app.users:
    return 'The user does not exist', 400

  if len( tweet ) > 300:
    return 'Exceeded the 300 character limit', 400

  user_id = int( payload['id'] )
  app.tweets.append( {
    'user_id': user_id,
    'tweet'  : tweet
  })
  return '', 200

@app.route( '/follow', methods=['POST'] )
def follow():
  payload           = request.json
  user_id           = int( payload['id'] )
  user_id_to_follow = int( payload['follow'] )

  if user_id not in app.users or user_id_to_follow not in app.users:
    return 'The user does not exist', 400

  user = app.users[ user_id ]
  user.setdefault( 'follow', set() ).add( user_id_to_follow )

  return jsonify( user )

@app.route('/unfollow', methods=['POST'])
def unfollow():
  payload           = request.json
  user_id           = int( payload['id'] )
  user_id_to_follow = int( payload['unfollow'] )

  if user_id not in app.users or user_id_to_follow not in app.users:
    return 'The user does not exist', 400

  user = app.users[ user_id ]
  user.setdefault( 'follow', set() ).discard( user_id_to_follow )

  return jsonify( user )

@app.route('/timeline/<int:user_id>', methods=['GET'])
def timeline( user_id ):
  if user_id not in app.users:
    return 'The user does not exist', 400

  follow_list = app.users[ user_id ].get( 'follow',set() )
  follow_list.add( user_id )
  timeline = [ tweet for tweet in app.tweets if tweet['user_id'] in follow_list ]

  return jsonify( {
    'user_id'  : user_id,
    'timeline' : timeline
  } )

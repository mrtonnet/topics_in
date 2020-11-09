# tweet.py
#
# * Draft: 2020-09-21 (Mon)
#
# Minitor's core functions
#   sign-up
#   log-in
#   tweet
#   follow
#   unfollow
#   timeline

from flask import Flask, jsonify, request

app          = Flask( __name__ )
app.users    = {} 
app.id_count = 1
app.tweets   = []

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



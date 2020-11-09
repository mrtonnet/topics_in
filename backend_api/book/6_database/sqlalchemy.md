* Draft: 2020-09-25 (Thu)

## SQLAlchemy를 사용하여 API와 데이터베이스 연결하기

SQLAlchemy는 Python에서 MySQL 데이터베이스와 연결하기 위한 라이브러리이다. DB와 연결하기 위해 사용하는 라이브러리 중 가장 널리 쓰이는 것 중에 하나이다.

아래는 미니터 백엔드API와 데이터베이스를 연결하는 코드를 본다. 참고로 코드가 복잡해지므로 오류 처리 로직이 구현되지 않았다. 교육용 코드이므로 괜찮지만, 상업용 시스템을 구현한다면 적절한 오류처리가 필요하다. 

`config.py`

```python
# config.py
# * Draft: 2020-09-22 (Tue)

db = {
  'user'     : 'root',
  'password' : 'test1234',
  'host'     : 'localhost',
  'port'     : 3306,
  'database' : 'miniter'
}

# mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}
DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
```

여기서 `password`를 로컬에 설치된 MySQL 서버의 root 패스워드로 변경해야 한다. 그러지 않으면 나중에 데이터베이스에 접촉이 필요할 때 `Access denied for user 'root'@'localhost'`에러가 발생한다.

```bash
  ...
sqlalchemy.exc.ProgrammingError: (mysql.connector.errors.ProgrammingError) 1698 (28000): Access denied for user 'root'@'localhost'
(Background on this error at: http://sqlalche.me/e/13/f405)
```

MySQL 5.7 (혹은 그 이상의 버전) 설치 시 주의할 점, pp.143~144 혹은  [error_1698-access_denied_for_user_root_localhost.md](../../../programming_languages/mysql/how_to_troubleshoot/error_1698-access_denied_for_user_root_localhost.md)를 참고해서 root password를 설정합니다. 터미널에서 `sudo` 명령어 없이 `mysql`명령어를 실행해서 MySQL 데이터베이스에 로그인을 해도 에러가 발생하지 않게 되면, 이 에러는 사라진다.

## 6장 데이터베이스 - 회원가입 엔드포인트, pp.159-162

### 소스코드 `sign_up_with_db.py`

```python
# sign_up_with_db.py
# * Draft: 2020-09-22 (Tue)

# Prerequisites:
#   1. Table users has already been created in a MySQL database.
#   2. Install 
#     $ pip install sqlalchemy
#     $ pip install mysql-connector-python

from flask      import Flask, jsonify, request
from sqlalchemy import create_engine, text

def create_app( test_config = None ):
  app = Flask( __name__ )

  if test_config is None:
    app.config.from_pyfile( "config.py" )
  else:
    app.config.update( test_config )

  database = create_engine( app.config['DB_URL'], encoding='utf-8', max_overflow=0 )
  app.database = database

  return app

app = create_app()

# For debugging
#app          = Flask( __name__ )

#-------------------------
#  Function definitions  #
#-------------------------
@app.route( '/ping', methods=[ 'GET' ] )
def ping():
  return 'pong'

@app.route( '/sign-up', methods=[ 'POST' ] )
def sign_up():
  new_user    = request.json
  # For debugging
  #print( new_user )
  #created_user = new_user

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

  row = app.database.execute( text("""
    SELECT
      id,
      name,
      email,
      profile
    FROM users
    WHERE id = :user_id
  """), {
    'user_id' : new_user_id
  }).fetchone()

  # To return the result to the client
  created_user = {
    'id'      : row['id'],
    'name'    : row['name'],
    'email'   : row['email'],
    'profile' : row['profile']
  } if row else None

#  created_user = new_user

  return jsonify( created_user )
```



### Client측

```bash
#!/bin/bash
# test_sign_up_with_db
# * Draft: 2020-09-22 (Tue)

http -v POST localhost:5000/sign-up name=user2 email=user2@email.com password=pw4user2 profile=myprofile2
```



```bash
$ ./test_sign_up_with_db
/usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.25.5) or chardet (3.0.4) doesn't match a supported version!
  RequestsDependencyWarning)
POST /sign-up HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 94
Content-Type: application/json
Host: localhost:5000
User-Agent: HTTPie/0.9.8

{
    "email": "user2@email.com",
    "name": "user2",
    "password": "pw4user2",
    "profile": "myprofile2"
}

HTTP/1.0 200 OK
Content-Length: 93
Content-Type: application/json
Date: Wed, 23 Sep 2020 13:16:10 GMT
Server: Werkzeug/1.0.1 Python/3.7.6

{
    "email": "user2@email.com",
    "id": 5,
    "name": "user2",
    "profile": "myprofile2"
}
$
```

### Server측

```bash
$ ./run_sign_up_with_db
 * Serving Flask app "sign_up_with_db.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 214-241-421
  ...
127.0.0.1 - - [23/Sep/2020 22:16:10] "POST /sign-up HTTP/1.1" 200 -
```



### 에러 메세지

#### 문제

즉, Client측의 명령어에 아래처럼 `profile`이 지정되어 있지 않으면, `A value is required for bind parameter 'profile'`이라는 에러가 발생합니다.

##### Client측 명령어

```bash
$ http -v POST localhost:5000/sign-up name=user1 email=user1@email.com password=pw4user1
```

##### Server측 에러 메세지

```bash
sqlalchemy.exc.InvalidRequestError: A value is required for bind parameter 'profile' (Background on this error at: http://sqlalche.me/e/13/cd3x)
```

#### 해결 방안

Client측 명령어에 `profile`에 값을 지정해주면 문제는 해결됩니다. 예를 들어,

```bash
$ http -v POST localhost:5000/sign-up name=user1 email=user1@email.com password=pw4user1 profile=myprofile1
```

#### 문제

데이터 베이스에 이미 가입이 되어 있는 user로 `sign-up`하려고 하면, `Duplicate entry`라고 알려준다.

##### Client측 명령어

```bash
$ http -v POST localhost:5000/sign-up name=user1 email=user1@email.com password=pw4user1 profile=myprofile1
```

##### Server측 에러 메세지

```bash
_mysql_connector.MySQLInterfaceError: Duplicate entry 'user1@email.com' for key 'email'
```

#### 해결 방안

* 이미 있는 사용자인 `user1@email.com`을 데이터베이스에서 지워야 합니다.

* 혹은 명령어 테스트만을 원한다면 새로운 사용자를 만들어주면 됩니다. 예를 들어 아래처럼 새로 `user2@email.com`을 만들어 줍니다.

```bash
$ http -v POST localhost:5000/sign-up name=user2 email=user2@email.com password=pw4user2 profile=myprofile2
```

## 6장 데이터베이스 - tweet 엔드포인트, pp.162-164

저장해야 하는 데이터인 Tweet결과를 HTTP Request를 통해 받아서 데이터베이스에 저장한다.

### API Server의 소스코드

```python
# tweet_with_db.py
#
# * Rev.1: 2020-09-24 (Thu)
# * Draft: 2020-09-21 (Mon)
#
# Minitor's core functions
#   sign-up
#   log-in
#   tweet

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
```

### Client측

```bash
#!/bin/bash
# test_tweet_with_db
# * Rev.1: 2020-09-24 (Thu)
# * Draft: 2020-09-21 (Mon)

http -v POST localhost:5000/tweet id=1 tweet="hello World"
```

### Server측 API Server

```bash
#!/bin/bash
#  run_tweet_with_db
# * Rev.1: 2020-09-24 (Thu)
# * Draft: 2020-09-21 (Mon)

# FLASK_ENV=development
#   turns on the debug mode.
#   When the .py file is changed, the change is applied on the fly.

FLASK_ENV=development FLASK_APP=tweet_with_db.py FLASK_DEBUG=1 flask run
```

```bash
$ ./run_tweet_with_db 
 * Serving Flask app "tweet_with_db.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 376-875-532
```

Client의 요청이 성공적으로 처리되었을 때의 메세지

```bash
127.0.0.1 - - [24/Sep/2020 09:22:10] "POST /tweet HTTP/1.1" 200 -
```

### Server측 Database

Tweet한 결과가 데이터베이스에 잘 쌓였는지 직접 확인해봅니다. 우선 서버 측의 MySQL 데이터베이스에 로그인합니다. 이 때 입력하는 password는 `config.py`에서 지정한 `test1234`와 동일합니다. 만약 다른 비밀번호를 지정했다면, 다른 비밀번호를 로그인합니다.

```bash
$ mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 5.7.31-0ubuntu0.18.04.1 (Ubuntu)

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

프롬프트가 `mysql>`로 변경되어 SQL 명령어를 입력받을 준비가 되었습니다. 

먼저 MySQL 데이터베이스 시스템에 있는 데이터베이스를 봅니다. 이 중에 `miniter`를 사용한다고 지정합니다.

```mysql
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| miniter            |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.01 sec)

mysql> USE miniter;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql>
```

어떤 테이블이 있는지 봅니다.

```
mysql> SHOW TABLES;
+-------------------+
| Tables_in_miniter |
+-------------------+
| tweets            |
| users             |
| users_follow_list |
+-------------------+
3 rows in set (0.00 sec)

mysql>
```

이 중 `tweets`테이블에 있는 결과를 모두 봅니다. SQL언어의 `SELECT`구문을 쓰면 테이블의 결과를 읽을 수 있습니다.

```mysql
mysql> SELECT * FROM tweets;
+----+---------+-------------+---------------------+
| id | user_id | tweet       | created_at          |
+----+---------+-------------+---------------------+
|  1 |       1 | hello World | 2020-09-24 09:22:10 |
+----+---------+-------------+---------------------+
1 row in set (0.01 sec)

mysql> 
```

1번 사용자의 `hello World`가 테이블에 들어있습니다.

재미삼아 다른 테이블의 내용도 확인해봅니다.

```mysql
mysql> SELECT * FROM users;
+----+-------+-----------------+-----------------+------------+---------------------+------------+
| id | name  | email           | hashed_password | profile    | created_at          | updated_at |
+----+-------+-----------------+-----------------+------------+---------------------+------------+
|  1 | user1 | user1@email.com | pw4user1        | myprofile1 | 2020-09-23 21:55:19 | NULL       |
|  5 | user2 | user2@email.com | pw4user2        | myprofile2 | 2020-09-23 22:16:10 | NULL       |
+----+-------+-----------------+-----------------+------------+---------------------+------------+
2 rows in set (0.00 sec)

mysql> SELECT * FROM users_follow_list;
Empty set (0.00 sec)

mysql> 
```

`users` 테이블에는 `user1`과 `user2` 두개의 레코드가 있습니다. `users_follow_list`는 아직 비어있습니다.

## `timeline` 엔드포인트

### Server측 

#### 소스코드

```python
# timeline_with_db.py
# * Rev.1: 2020-09-24 (Thu)
# * Draft: 2020-09-21 (Mon)

# Prerequisites:
#   1. Table users has already been created in a MySQL database.
#   2. Install 
#     $ pip install sqlalchemy
#     $ pip install mysql-connector-python

from flask      import Flask, jsonify, request
from sqlalchemy import create_engine, text

def create_app( test_config = None ):
  app = Flask( __name__ )

  if test_config is None:
    app.config.from_pyfile( "config.py" )
  else:
    app.config.update( test_config )

  database = create_engine( app.config['DB_URL'], encoding='utf-8', max_overflow=0 )
  app.database = database

  return app

app = create_app()

# For debugging
#app          = Flask( __name__ )

#-------------------------
#  Function definitions  #
#-------------------------
@app.route( '/ping', methods=[ 'GET' ] )
def ping():
  return 'pong'

@app.route( '/sign-up', methods=[ 'POST' ] )
def sign_up():
  new_user    = request.json
  # For debugging
  #print( new_user )
  #created_user = new_user

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

  row = app.database.execute( text("""
    SELECT
      id,
      name,
      email,
      profile
    FROM users
    WHERE id = :user_id
  """), {
    'user_id' : new_user_id
  }).fetchone()

  # To return the result to the client
  created_user = {
    'id'      : row['id'],
    'name'    : row['name'],
    'email'   : row['email'],
    'profile' : row['profile']
  } if row else None
#  For debugging
#  created_user = new_user

  return jsonify( created_user )

@app.route( '/tweet',methods=['POST'] )
def tweet():
  user_tweet = request.json
  tweet      = user_tweet[ 'tweet' ]
  
  if len( tweet ) > 300:
    return 'Exceeded the 300 character limit', 400

  app.database.execute( text("""
    INSERT INTO tweets (
      user_id,
      tweet
    ) VALUES (
      :id,
      :tweet
    )
   """), user_tweet )

  return '', 200

@app.route( '/timeline/<int:user_id>', methods=['GET'] )
def timeline( user_id ):
  rows = app.database.execute( text("""
    SELECT
      t.user_id,
      t.tweet
    FROM tweets t
    LEFT JOIN users_follow_list ufl ON ufl.user_id = :user_id
    WHERE t.user_id = :user_id
    OR t.user_id = ufl.follow_user_id
  """), {
    'user_id' : user_id
  }).fetchall()


  timeline = [{
    'user_id' : row['user_id'],
    'tweet' : row['tweet']
  } for fow in rows]

  return jsonify({
    'user_id' : user_id,
    'timeline' : timeline
  })
```

#### 코드 실행 명령어

```bash
#!/bin/bash
#  run_timeline_with_db
# * Rev.1: 2020-09-24 (Thu)
# * Draft: 2020-09-21 (Mon)

# FLASK_ENV=development
#   turns on the debug mode.
#   When the .py file is changed, the change is applied on the fly.

FLASK_ENV=development FLASK_APP=timeline_with_db.py FLASK_DEBUG=1 flask run
```

```bash
$ ./run_timeline_with_db
 * Serving Flask app "timeline_with_db.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 905-405-569
```

### Client측

#### 테스트 코드

```bash
#!/bin/bash
# test_timeline_with_db
# * Rev.1: 2020-09-24 (Thu)
# * Draft: 2020-09-21 (Mon)

http -v GET localhost:5000/timeline/1
```

#### HTTP 요청 실행

HTTP 요청을 했을 때 아래와 같은 메세지가 발생한다.

```bash
$ ./test_timeline_with_db 
GET /timeline/1 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/0.9.8
```

#### Problem: `500 INTERNAL SERVER ERROR`

Client측의 응답에는 `500 INTERNAL SERVER ERROR`에러가 발생했습니다. 제일 밑 쪽을 보면 `row`가 정의되어 있지 않다고 합니다.

```bash
HTTP/1.0 500 INTERNAL SERVER ERROR
Connection: close
Content-Type: text/html; charset=utf-8
Date: Thu, 24 Sep 2020 00:56:28 GMT
Server: Werkzeug/1.0.1 Python/3.7.6
X-XSS-Protection: 0
  ...
Traceback (most recent call last):
  File "/home/aimldl/anaconda3/lib/python3.7/site-packages/flask/app.py", line 2464, in __call__
  ...
  File "/home/aimldl/projects/api/timeline_with_db.py", line 122, in <listcomp>
    } for fow in rows]
NameError: name 'row' is not defined

-->
```

서버측 로그에도 동일한 에러가 있습니다.

```bash
127.0.0.1 - - [24/Sep/2020 09:56:28] "GET /timeline/1 HTTP/1.1" 500 -
  ...
File "/home/aimldl/projects/api/timeline_with_db.py", line 122, in <listcomp>
    } for fow in rows]
NameError: name 'row' is not defined
```

#### Hint

`timeline_with_db.py` 코드를 보니 오타가 있었습니다.

#### Solution

 `fow`를 `row`로 수정하고 저장하면,

```bash
# Before
  } for fow in rows]
# After
  } for row in rows]
```

API Server가 자동으로 코드를 reload했습니다.

```bash
 * Detected change in '/home/aimldl/projects/api/timeline_with_db.py', reloading
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 906-008-021
```

다시 Client에서 HTTP 요청을 하고, `200 OK` 응답을 받았습니다.

#### Client측 HTTP 요청

```
$ ./test_timeline_with_db
GET /timeline/1 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/0.9.8



HTTP/1.0 200 OK
Content-Length: 103
Content-Type: application/json
Date: Thu, 24 Sep 2020 01:19:17 GMT
Server: Werkzeug/1.0.1 Python/3.7.6

{
    "timeline": [
        {
            "tweet": "hello World",
            "user_id": 1
        }
    ],
    "user_id": 1
}


```

timeline의 JSON 데이터가 응답으로 왔습니다. 현재는 `user_id` 1의 `hello World`라는 내용의 `tweet` 밖에 없습니다.

#### Server측 로그

```bash
127.0.0.1 - - [24/Sep/2020 10:19:17] "GET /timeline/1 HTTP/1.1" 200 -
```



## app_with_db.py

이 장의 최종 코드는 `app.py`으로 앞장의 파일과 구분하기 위해서  `app_with_db.py`으로 이름을 변경했습니다. 전체 코드는 내용의 가독성을 위해 이 세션의 뒷부분에 있습니다.

```python
# app_with_db.py
  ...
def create_app( test_config = None ):
  ...
#---------
#  Main  #
#---------
app = create_app()
```

코드에 정의된 `create_app`함수는 정의가 됐지만 호출이 되지 않았습니다.  즉, `app = create_app()`과 같이 함수가 실행되는 부분이 없습니다. 

### test_ping 엔드포인트

`app_with_db.py`를 서버 측에서 실행하는 명령어를 써서

```bash
#!/bin/bash
#  run_app_with_db
# * Rev.1: 2020-09-24 (Thu)
# * Draft: 2020-09-21 (Mon)

# FLASK_ENV=development
#   turns on the debug mode.
#   When the .py file is changed, the change is applied on the fly.

FLASK_ENV=development FLASK_APP=app_with_db.py FLASK_DEBUG=1 flask run
```

미니터 API서버를 실행하고

```
$ ./run_app_with_db
 * Serving Flask app "app_with_db.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-601-410

```

client에서 ping으로 동작여부를 테스트하면 HTTP 응답이 `200 OK`로 정상작동 함을 알 수 있습니다.

```bash
$ ./test_ping 
http -v GET localhost:5000/ping
GET /ping HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/0.9.8



HTTP/1.0 200 OK
Content-Length: 4
Content-Type: text/html; charset=utf-8
Date: Thu, 24 Sep 2020 04:40:43 GMT
Server: Werkzeug/1.0.1 Python/3.7.6

pong

$
```

서버 측 로그의 예는 다음과 같습니다.

```bash
127.0.0.1 - - [24/Sep/2020 13:40:43] "GET /ping HTTP/1.1" 200 -
```

참고로 이 단계에서 오타, 잘못된 띄워쓰기 등 사소한 이유로 에러가 발생할 수 있습니다. `ping`의 경우 수행 로직이 단순하므로 에러가 난 부분을 수정합니다. 

### `sign-up` 엔드포인트

```bash
$ ./test_sign_up_with_db
http -v POST localhost:5000/sign-up name=user3 email=user3@email.com password=pw4user3 profile=myprofile3
POST /sign-up HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 94
Content-Type: application/json
Host: localhost:5000
User-Agent: HTTPie/0.9.8

{
    "email": "user3@email.com",
    "name": "user3",
    "password": "pw4user3",
    "profile": "myprofile3"
}

HTTP/1.0 200 OK
Content-Length: 93
Content-Type: application/json
Date: Thu, 24 Sep 2020 04:50:16 GMT
Server: Werkzeug/1.0.1 Python/3.7.6

{
    "email": "user3@email.com",
    "id": 7,
    "name": "user3",
    "profile": "myprofile3"
}
$
```

### tweet 엔드포인트

#### Client측 

```bash
$ ./test_tweet_with_db
http -v POST localhost:5000/tweet id=1 tweet="hello world"
POST /tweet HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 35
Content-Type: application/json
Host: localhost:5000
User-Agent: HTTPie/0.9.8

{
    "id": "1",
    "tweet": "hello world"
}

HTTP/1.0 200 OK
Content-Length: 0
Content-Type: text/html; charset=utf-8
Date: Thu, 24 Sep 2020 05:16:45 GMT
Server: Werkzeug/1.0.1 Python/3.7.6
$
```

#### API Server측 로그

```bash
127.0.0.1 - - [24/Sep/2020 14:16:45] "POST /tweet HTTP/1.1" 200 -
```

#### 데이터베이스의 테이블 내용 확인

```bash
$ mysql -uroot -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 15
Server version: 5.7.31-0ubuntu0.18.04.1 (Ubuntu)

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| miniter            |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)

mysql> USE miniter;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> SHOW TABLES;
+-------------------+
| Tables_in_miniter |
+-------------------+
| tweets            |
| users             |
| users_follow_list |
+-------------------+
3 rows in set (0.00 sec)

mysql> SELECT * FROM tweets;
+----+---------+-------------+---------------------+
| id | user_id | tweet       | created_at          |
+----+---------+-------------+---------------------+
|  1 |       1 | hello World | 2020-09-24 09:22:10 |
|  2 |       1 | hello world | 2020-09-24 14:16:02 |
+----+---------+-------------+---------------------+
2 rows in set (0.00 sec)

mysql> exit
Bye
$
```

### timeline 엔드포인트

#### run_timeline_with_db

```bash
#!/bin/bash
# run_timeline_with_db
# * Rev.1: 2020-09-24 (Thu)
# * Draft: 2020-09-21 (Mon)

# FLASK_ENV=development
#   turns on the debug mode.
#   When the .py file is changed, the change is applied on the fly.

run() {
  command=$1
  echo $command
  eval $command
}

run 'FLASK_ENV=development FLASK_APP=timeline_with_db.py FLASK_DEBUG=1 flask run'
```

#### Server측

```bash
$ ./run_timeline_with_db 
FLASK_ENV=development FLASK_APP=timeline_with_db.py FLASK_DEBUG=1 flask run
 * Serving Flask app "timeline_with_db.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 228-238-654
```

#### Client측

```bash
$ ./test_timeline_with_db
http -v GET localhost:5000/timeline/1
GET /timeline/1 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/0.9.8



HTTP/1.0 200 OK
Content-Length: 231
Content-Type: application/json
Date: Thu, 24 Sep 2020 05:29:02 GMT
Server: Werkzeug/1.0.1 Python/3.7.6

{
    "timeline": [
        {
            "tweet": "hello World",
            "user_id": 1
        },
        {
            "tweet": "hello World",
            "user_id": 1
        },
        {
            "tweet": "hello world",
            "user_id": 1
        }
    ],
    "user_id": 1
}
$
```

### Server측 Log

```bash
127.0.0.1 - - [24/Sep/2020 14:43:13] "GET /timeline/1 HTTP/1.1" 200 -
```

## app_with_db.py 전체 코드

```python
# app_with_db.py
#   This Python script is to run a Flask server for miniter with MySQL Database. 
#
# * Draft: 2020-09-24 (Thu)
#
# This code is from:
#   '깔끔한 파이썬 탄탄한 백엔드', '6장 데이터베이스', 송은우 지음, pp.167-171
#   https://github.com/rampart81/python-backend-book/blob/master/chapter6/app.py

from flask      import Flask, request, jsonify, current_app
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text

# Custom Class Definition

class CustomJSONEncoder( JSONEncoder ):
  def default( self, obj ):
    if isinstance( obj, set ):
      return list( obj )

    # else
    return JSONENcoder.default( self, obj )

# Function Definitions

def get_user( user_id ):
  user = current_app.database.execute( text("""
    SELECT
      id,
      name,
      email,
      profile
    FROM users
    WHERE id = :user_id
  """), {
    'user_id' : user_id
  }).fetchone()

  return {
    'id'      : user['id'],
    'name'    : user['name'],
    'email'   : user['email'],
    'profile' : user['profile'],
  } if user else None

def insert_user( user ):
  return current_app.database.execute( text("""
    INSERT INTO users (
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
  """), user ).lastrowid

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

def get_timeline( user_id ):
  timeline = current_app.database.execute( text("""
    SELECT
      t.user_id,
      t.tweet
    FROM tweets t
    LEFT JOIN users_follow_list ufl ON ufl.user_id = :user_id
    WHERE t.user_id = :user_id
  """), { 'user_id' : user_id }).fetchall()

  return [{
    'user_id' : tweet[ 'user_id' ],
    'tweet'   : tweet[ 'tweet' ]
  } for tweet in timeline]

def create_app( test_config = None ):
  app = Flask( __name__ )

  app.json_encoder = CustomJSONEncoder

  if test_config is None:
    app.config.from_pyfile( 'config.py' )
  else:
    app.config.update( test_config )

  database = create_engine( app.config['DB_URL'], encoding='utf-8', max_overflow=0 )
  app.database = database

  @app.route('/ping', methods=['GET'])
  def ping():
    return "pong"

  @app.route('/sign-up', methods=['POST'])
  def sign_up():
    new_user    = request.json
    new_user_id = insert_user( new_user )
    new_user    = get_user( new_user_id )

    return jsonify( new_user )

  @app.route('/tweet', methods=['POST'])
  def tweet():
    user_tweet = request.json
    tweet      = user_tweet['tweet']

    if len(tweet) > 300:
      return 'Exceeded the 300 character limit', 400

    insert_tweet( user_tweet )

    return '', 200

  @app.route('/follow', methods=['POST'])
  def follow():
    payload = request.json
    insert_follow( payload )
    return '', 200

  @app.route('/unfollow', methods=['POST'])
  def unfollow():
    payload = request.json
    insert_unfollow( payload )
    return '', 200

  @app.route('/timeline/<int:user_id>', methods=['GET'])
  def timeline( user_id ):
    return jsonify({
      'user_id'  : user_id,
      'timeline' : get_timeline( user_id )
    })

  return app
```


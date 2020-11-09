* Draft: 2020-09-21 (Mon)

# 7. 인증 (Authentication)

인증은 사용자의 신원을 확인하는 절차입니다. 사용자 신원 (User Identification)은 로그인을 위해 입력한 ID와 비밀번호를 확인하게 됩니다. 로그인 기능을 인증 엔드포인트에서 구현하게 됩니다.

인증 엔드포인트는 많은 API에서 공통적으로 구현됩니다. 미니터 API에 인증 절차를 구현하고 비밀번호를 암호화합니다.

* 인증 (Authentication)
* 사용자 비밀번호 암호화
* Bcrypt
* JWT (JSON Web Tokens)

## 비밀번호 암호화

### 단방향 해시 함수 (One-way Hash Function)를 이용한 비밀번호 암호화

```bash
$ python
Python 3.7.6 (default, Jan  8 2020, 19:59:22) 
[GCC 7.3.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import hashlib
>>> m = hashlib.sha256()
>>> m.update( b'test password' )
>>> m.hexdigest()
'0b47c69b1033498d5f33f5f7d97bb6a3126134751629f4d0185c115db44c094e'
>>> 

```

### bcrypt 암호 알고리즘

단방향 해시 함수의 취약점을 보완하기 위해 일반적으로 2가지 방법이 사용됩니다. 

* Salting
* 키 스트레칭 (Key Stretching)

이 2가지 방식을 구현한 해시 함수 중 `bcrypt`가 가장 널리 사용됩니다.

#### Python 모듈 설치

```bash
$ pip install bcrypt
```

#### 사용예

```bash
$ python
Python 3.7.6 (default, Jan  8 2020, 19:59:22) 
[GCC 7.3.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import bcrypt
>>> bcrypt.hashpw( b'secrete password', bcrypt.gensalt() )
b'$2b$12$7kgXaHRegsibhAf3pKw3nO0EX/A4qko/gyvXJWSzJk3uKwN5UlKBK'
>>> bcrypt.hashpw( b'secrete password', bcrypt.gensalt() ).hex()
'2432622431322476485531322f6a4d5976786356565464324136662f4f6131504e4831364e4a6f437a38773663335845626a4637626d524a32713736'
>>> 

```

### Access Token

* HTTP는 stateless이므로 현재 HTTP통신에서 이전에 이미 인증이 되었는지 알지 못합니다. 
* 그래서 HTTP 요청을 처리하기 위해서, 필요한 모든 데이터를 첨부해야 합니다.
* 즉, 로그인 정보 또한 첨부해서 보내야 API서버는 해당 사용자가 이미 로그인된 상태임을 알 수 있습니다.
* Access Token에 이러한 로그인 정보를 담게 됩니다.

#### Access Token의 흐름

* API서버에서 사용자의 로그인 정보를 access token형태로 생성해서 프론트엔드 서버에 전송
* 프론트엔드 서버는 access token을 전송받은 access token을 그대로 다시 백엔드 서버에 HTTP 요청을 보낼 때 첨부해서 전송
* 백엔드 API서버는 프론트엔드가 보내준 access token을 통해 해당 사용자의 로그인 여부를 알 수 있음

[TODO: 표현을 다르게 해서 적을 것]





### PyJWT

##### 설치하기

```bash
(api) $ api pip install PyJWT
Collecting PyJWT
  Using cached PyJWT-1.7.1-py2.py3-none-any.whl (18 kB)
Installing collected packages: PyJWT
Successfully installed PyJWT-1.7.1
(api) $
```

##### 인코딩 및 디코딩 예제

```bash
(api) $ python
Python 3.8.5 (default, Sep  4 2020, 07:30:14) 
[GCC 7.3.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import jwt
>>> data_to_encode = {'some':'payload'}
>>> encryption_secret = 'secrete'
>>> algorithm = 'HS256'
```

HS256 알고리즘을 써서 `secret`이라는 비밀 키 (secret key)를 지정하고, payload에 들어갈 JSON 데이터를 `data_to_encode`에 저장한다. 인코딩된 JWT, 즉 토큰은 아래와 같이 3개 부분으로 구성된다. 

```bash
>>> encoded = jwt.encode( data_to_encode, encryption_secret, algorithm=algorithm )
>>> encoded
b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.j4hydZvraNFUqUHpXw0hYBN9qTRzbm9-yS9h5skNht0'
```

디코딩을 하면 payload에 있는 JSON 데이터가 복원된다.

```bash
>>> jwt.decode( encoded, encryption_secret, algorithms=[algorithm] )
{'some': 'payload'}
>>> 
```

## 다음

* [인증 엔드포인트 구현하기](login_required_decorator.md)
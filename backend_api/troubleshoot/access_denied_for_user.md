* Draft: 2020-09-23 (Wed)

# ERROR 1698 (28000): Access denied for user 'root'@'localhost'

* SQLAlchemy를 사용하여 API와 데이터베이스 연결하기

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

## Problem

SQLAlchemy로 데이터베이스에 접속할 때 `(28000): Access denied for user 'root'@'localhost'`에러가 발생한다.

```bash
  ...
sqlalchemy.exc.ProgrammingError: (mysql.connector.errors.ProgrammingError) 1698 (28000): Access denied for user 'root'@'localhost'
(Background on this error at: http://sqlalche.me/e/13/f405)
```

## Hint

* 우선 `config.py`의 `password`를 로컬에 설치된 MySQL 서버의 root 패스워드로 변경해야 한다.
* 패스워드 변경 후에도 `(28000): Access denied`에러가 발생하므로, `mysql`명령어를 실행해서 확인해본다.

```bash
$ sudo mysql -u root -p
[sudo] password for aimldl: 
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 14
Server version: 5.7.31-0ubuntu0.18.04.1 (Ubuntu)

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
```

왜 `mysql`명령어는 되는데, `SQLAlchemy`는 안 될까? `sudo`명령어 없이 실행할 경우

```bash
$ mysql -u root -p 
Enter password: 
ERROR 1698 (28000): Access denied for user 'root'@'localhost'
$
```

발생하는 에러가 Python의 SQLAlchemy에서 발생한 것과 동일하다!

### SQLAlchemy의 에러

```bash
... 1698 (28000): Access denied for user 'root'@'localhost'
```

### MySQL의 실행 에러

```bash
ERROR 1698 (28000): Access denied for user 'root'@'localhost'
```


# config.py
# * Draft: 2020-09-22 (Tue)

# password must be identical to MySQL's root password.
db = {
  'user'     : 'root',
  'password' : 'test1234',
  'host'     : 'localhost',
  'port'     : 3306,
  'database' : 'miniter'
}

# mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}
DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

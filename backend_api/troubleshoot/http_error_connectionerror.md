* Draft: 2020-09-24 (Tue)

# http: error: ConnectionError

## Problem

`http: error: ConnectionError`가 발생했다.

```bash
$ ./test_timeline_with_db 
http -v GET localhost:5000/timeline/1

http: error: ConnectionError: HTTPConnectionPool(host='localhost', port=5000): Max retries exceeded with url: /timeline/1 (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7fc215c01f60>: Failed to establish a new connection: [Errno 111] Connection refused',)) while doing GET request to URL: http://localhost:5000/timeline/1
$
```

## Solution

원인은 단지 API서버가 실행되지 않고 있었기 때문인데, 서버를 실행하면 문제가 쉽게 해결됩니다.

### Server측

```bash
$ ./run_timeline_with_db 
 * Serving Flask app "timeline_with_db.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 294-878-070
127.0.0.1 - - [24/Sep/2020 14:29:02] "GET /timeline/1 HTTP/1.1" 200 -
```

### Client측

```bash
$ ./test_timeline_with_db
http -v GET localhost:5000/timeline/1
/usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.25.5) or chardet (3.0.4) doesn't match a supported version!
  RequestsDependencyWarning)
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


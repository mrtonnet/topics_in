* Draft: 2020-09-21 (Mon)

## FLASK_ENV=development

디버그 모드를 켜는 옵션입니다.

```bash
#!/bin/bash
#  run_unfollow
#  * Draft: 2020-09-21 (Mon)

# FLASK_ENV=development
#   turns on the debug mode.
#   When miniter.py is changed, the change is applied on the fly.

FLASK_ENV=development FLASK_APP=unfollow.py FLASK_DEBUG=1 flask run
```

이미 소스코드 `unfollow.py`가 실행되고 있어도, 파일의 내용을 수정하면 소스코드를 `reload`할 수 있습니다.

아래의 예는 `/unfollow` 엔드포인트에서 에러가 나서 소스코드를 수정하고 파일을 저장했을 때, 자동으로 `reload`되는 메세지를 보여줍니다.

```bash
 $ ./run_unfollow 
 * Serving Flask app "unfollow.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 261-426-700
127.0.0.1 - - [21/Sep/2020 13:51:10] "POST /sign-up HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 13:51:10] "POST /tweet HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 13:51:11] "POST /follow HTTP/1.1" 400 -
127.0.0.1 - - [21/Sep/2020 13:51:11] "POST /unfollow HTTP/1.1" 500 -
  ...
KeyError: 'follow'
 * Detected change in '/home/aimldl/projects/api/unfollow.py', reloading
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 291-616-974
```


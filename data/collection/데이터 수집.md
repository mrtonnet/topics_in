# 데이터 수집

## 파이썬을 이용해서 파일을 다운로드

### urllib.request로 다운로드하기

import urllib.request

url = "http://uta.pw/shodu/img/28/214.png"

savename = "test.png"

urllib.request.urlretrieve( url, savename )

print(f"{savename} is saved.")



https://finance.naver.com/marketindex/

from bs4 import BeautifulSoup

import urllib.request as req

url = "https://finance.naver.com/marketindex/"

res = req.urlopen( url )

soup = BeautifulSoup( res, "html.parser")

price = soup.select_one("div.head_info > span.value").string

print( "USD/KRW = ", price )





스크레이핑할 때 굉장히 유용한 기능을 알아봅니다.

[https://ko.wikisource.org/wiki/%EC%A0%80%EC%9E%90:%EC%9C%A4%EB%8F%99%EC%A3%BC](https://ko.wikisource.org/wiki/저자:윤동주)



마우스 우클릭 "Copy > Copy Element"

> ```
> <span style="font-size:115%;"><b>윤동주</b></span>
> ```

마우스 우클릭 "Copy > Copy selector"

#mw-content-text > div > ul:nth-child(6) > li > b

```

```





```
<b><a href="/wiki/%ED%95%98%EB%8A%98%EA%B3%BC_%EB%B0%94%EB%9E%8C%EA%B3%BC_%EB%B3%84%EA%B3%BC_%EC%8B%9C" title="하늘과 바람과 별과 시">하늘과 바람과 별과 시</a></b>
```

```
<a href="/wiki/%ED%95%98%EB%8A%98%EA%B3%BC_%EB%B0%94%EB%9E%8C%EA%B3%BC_%EB%B3%84%EA%B3%BC_%EC%8B%9C" title="하늘과 바람과 별과 시">하늘과 바람과 별과 시</a>
```


* Rev.1: 2020-05-25 (Mon)
* Draft: 2016-09-02 (Fri)
# Web Crawler
A webcrawler is conceptually simple, but implementing it is not so simple.

## The basic algorithm
is simple. It revolves around a FIFO queue data structure which stores pending URLs.
```
1. Begin with a base URL that you select, and place it on the top of your queue
2. Pop the URL at the top of the queue and download it
3. Parse the downloaded HTML file and extract all links
4. Insert each extracted link into the queue
5. Goto step 2, or stop once you reach some specified limit
```
(If C++ is used,) C++ has a built-in queue structure in the standard libary, std::queue, which you can use to store URLs as strings.

## Implementation
is not so simple.
```
1. HTTP Networking Library
2. HTML Parser
3. Politeness
4. Avoid repeated websites
5. Multi threading
6. Multiprocessing
7. Efficient data structure
8. DB design
```
Obey the [robots exclusion protocol](https://en.wikipedia.org/wiki/Robots_exclusion_standard), avoid crawler traps, etc... All these details add up to make actually implementing a robust webcrawler not such a simple thing.

The raw-performance and low-level access you get in C++ is useless when writing a program like a webcrawler, which spends most of its time waiting for URLs to resolve and download. A higher-level scripting language like Python or something is better suited for this task, in my opinion.

### 3. Politeness
There are also other considerations you need to take into account when writing a webcrawler, such as politeness. People will be pissed and possibly ban your IP if you attempt to download too many pages, too quickly, from the same host. So you may need to implement some sort of policy where your webcrawler waits for a short period before downloading each site.

### 4. Avoid repetition
You also need some mechanism to avoid downloading the same URL again.

For details, refer to http://stackoverflow.com/questions/4278024/a-very-simple-c-web-crawler-spider

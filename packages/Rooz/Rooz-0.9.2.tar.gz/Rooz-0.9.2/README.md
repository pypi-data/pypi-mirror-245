# Rooz 

Python functions for Search and DownLoad From Social Media .


But first of all, you must follow this important step :

```pip install youtube-search```

## Examples : 

## Download from threads :

```python
from Rooz import Download

result = Download('https://www.threads.net/@meta/post/C0e7bZquTL6').DownThreads()

print(result)
```


## Download from facebook :


```python
from Rooz import Download

result = Download('https://fb.watch/oROwmnBEM-/?mibextid=Nif5oz').DownFaceBook()

print(result)

```


## Download from Pinterest:


```python
from Rooz import Download

result = Download('https://pin.it/5TkWcys').DownPinterest()
print(result)

```

## Download from SoundCloud:


```python
from Rooz import Download

result = Download('https://soundcloud.com/akon/lonely-old-version').DownSoundCloud()
print(result)

```

## Download from TikTok:


```python
from Rooz import Download

result = Download('https://vm.tiktok.com/ZM6YyohK6/').DownTikTok()
print(result)

```

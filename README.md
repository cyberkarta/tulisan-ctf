## CTF Speedrun

## Forensic
### Windows Registry
Tools primer: 
- regripper
	- Cari `Run` dan `RunOce`

Tools sekunder: reglookup


## Web
Apabila White Box (source code terlihat)
1. Untuk web dengan MVC, lebih mudah apabila serangan dimulai dari routes. Fungsinya untuk mengetahui endpoint, contoh `views/alien.html`
2. Coba kunjungi endpoint tersebut `http://target.com/alien.html`
3. Pahami code yang tertampil pada code dan implementasinya pada browser.
4. Jangan lupa lihat browser console untuk informasi error.


Halaman yang hanya bisa diakses oleh IP localhost (127.0.0.1), serangan yang mungkin dilakukan:
- Cross-site scripting untuk mengambil data yang terlihat oleh admin.
- X-Forwarded-For dengan menggunakan IP 127.0.0.1.
- Server Side Request Forgery untuk membuka IP tersebut.


Sumber:
https://www.youtube.com/watch?v=JEdkDzfqgzw&t=441s


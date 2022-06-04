# Cara Build Docker Image

- Unzip file challenge pada masing-masing challenge.  
![](attachments/Pasted%20image%2020220604115812.png)

- Buka Dockerfile di dalam folder hasil ekstrak zip dan ganti `FROM alpine:edge` menjadi `From alpine:3.15`.  Kemudian tutup file tersebut.
![](attachments/Pasted%20image%2020220604115924.png)

- Jalankan `docker build .` di dalam folder tersebut dan tunggu hingga proses selesai.

- Buka `docker images` dan dapatkan value dari `IMAGE ID` yang sesuai.  
![](attachments/Pasted%20image%2020220604120556.png)

- Buat tag dengan `docker tag <IMAGE ID> htb/challenge`. Contohnya `docker tag 3369da3c8bc3 htb/intergalactic_post`

- Sekarang cek dengan perintah `docker images` kembali, pastikan tag nya sudah berganti

- Jalankan dengan perintah `docker run -d -p 1337:80 <TAG YANG SUDAH DIBUAT>` . Contohnya `docker run -d -p 1337:80 htb/intergalactic_post` .

- Docker akan bisa diakses melalui port 1337.  Untuk list proses docker yang berjalan bisa melalui `docker ps` .
![](attachments/Pasted%20image%2020220604120909.png)

- (Optional) Mengganti docker name di bawah ini dengan menggunakan `docker rename practical_goldstine web_intergalactic_post` .
![](attachments/Pasted%20image%2020220604122039.png)

- (Optional) Apabila ingin interactive shell di dalam docker, bisa menggunakan `docker exec -it web_intergalactic_post /bin/sh` .  
![](attachments/Pasted%20image%2020220604122336.png)


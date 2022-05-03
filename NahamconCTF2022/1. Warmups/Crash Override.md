# Crash Override
#easy #bufferoverflow

Tantangan ini adalah buffer overflow sederhana dengan mengeksploitasi fungsi `gets`.

File: ![](attachments/crash_override.c)
![](attachments/Makefile)

![](attachments/crash_override)

## Tantangan
- Saat mencoba koneksi
![](attachments/Pasted%20image%2020220501221628.png)

- Source code C yang berjalan pada server
![](attachments/Pasted%20image%2020220501221322.png)
Pada fungsi `main` terdapat variabel bernama buffer berupa karakter sebanyak 2048. Namun variabel buffer ini dipakai pada fungsi `gets` yang rentan terhadap buffer overflow.

## Solusi
- Kita perlu membuat karakter dengan jumlah lebih dari 2048 agar buffer overflow ini berjalan. Kita bisa gunakan `openssl`, sebagai contoh:

![](attachments/Pasted%20image%2020220501221207.png)

- Buat 2500 karakter dengan menggunakan `openssl`, dan masukkan hasilnya ke dalam clipboard
```sh
openssl rand -hex 2500 | xsel -ib
```

- Masuk ke dalam challenge dan paste
![](attachments/Pasted%20image%2020220501220957.png)


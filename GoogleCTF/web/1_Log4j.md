# Log4J
#web #easy #informationdisclosure 

web: https://log4j-web.2022.ctfcompetition.com/

## Tantangan
- Terdapat sebuah web yang berisi sebuah formulir chatbot.

![](attachments/Pasted%20image%2020220708110319.png)  
- Disediakan source code.
- Di dalam challenge tersebut juga terdapat docker image yang dapat dijalankan dengan perintah di bawah ini.
```sh
docker run --cap-add=SYS_ADMIN --read-only --security-opt apparmor=unconfined --security-opt seccomp=unconfined -d -p 1337:1337 gctf/log4j
```

## Source Code
- app.py
```python
import os
import subprocess

from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        text = request.form['text'].split(' ')
        cmd = ''
        if len(text) < 1:
            return ('invalid message', 400)
        elif len(text) < 2:
            cmd = text[0]
            text = ''
        else:
            cmd, text = text[0], ' '.join(text[1:])
        result = chat(cmd, text)
        return result
    return render_template('index.html')

def chat(cmd, text):
    # run java jar with a 10 second timeout
    res = subprocess.run(['java', '-jar', '-Dcmd=' + cmd, 'chatbot/target/app-1.0-SNAPSHOT.jar', '--', text], capture_output=True, timeout=10)
    print(res.stderr.decode('utf8'))
    return res.stdout.decode('utf-8')

if __name__ == '__main__':
    port = os.environ['PORT'] if 'port' in os.environ else 1337
    app.run(host='0.0.0.0', port=port)
```

- App.java
```java
package com.google.app;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import java.lang.System;
import java.time.format.DateTimeFormatter;
import java.time.LocalDateTime;
import java.util.Arrays;

public class App {
  public static Logger LOGGER = LogManager.getLogger(App.class);
  public static void main(String[]args) {
    String flag = System.getenv("FLAG");
    if (flag == null || !flag.startsWith("CTF")) {
        LOGGER.error("{}", "Contact admin");
    }
  
    LOGGER.info("msg: {}", args);
    // TODO: implement bot commands
    String cmd = System.getProperty("cmd");
    if (cmd.equals("help")) {
      doHelp();
      return;
    }
    if (!cmd.startsWith("/")) {
      System.out.println("The command should start with a /.");
      return;
    }
    doCommand(cmd.substring(1), args);
  }

  private static void doCommand(String cmd, String[] args) {
    switch(cmd) {
      case "help":
        doHelp();
        break;
      case "repeat":
        System.out.println(args[1]);
        break;
      case "time":
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/M/d H:m:s");
        System.out.println(dtf.format(LocalDateTime.now()));
        break;
      case "wc":
        if (args[1].isEmpty()) {
          System.out.println(0);
        } else {
          System.out.println(args[1].split(" ").length);
        }
        break;
      default:
        System.out.println("Sorry, you must be a premium member in order to run this command.");
    }
  }
  private static void doHelp() {
    System.out.println("Try some of our free commands below! \nwc\ntime\nrepeat");
  }
}

```

- log4j2.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="INFO">
    <Appenders>
        <Console name="Console" target="SYSTEM_ERR">
            <PatternLayout pattern="%d{HH:mm:ss.SSS} %-5level %logger{36} executing ${sys:cmd} - %msg %n">
            </PatternLayout>
        </Console>
    </Appenders>
    <Loggers>
        <Root level="debug">
            <AppenderRef ref="Console"/>
        </Root>
    </Loggers>
</Configuration>

```

- Dan juga pada pom.xml, kita bisa dapatkan bahwa log4j yang digunakan adalah versi 2.17.2, versi Log4j ini secara default menolak permintaan eksploitasi JNDI.
```xml
<!-- lines -->

 <dependency>
        <groupId>org.apache.logging.log4j</groupId>
        <artifactId>log4j-core</artifactId>
        <version>2.17.2</version>
    </dependency>
    
<!-- lines -->
```

## Solusi
Chatbot ini ternyata bisa menjalankan beberapa perintah yang dimasukkan oleh user, yaitu 
`help`, `/wc`, `/repeat`, dan `/time`.  
![](attachments/Pasted%20image%2020220708110803.png)  

- Aplikasi Java ini tidak bisa dieksploitasi dengan JNDI, karena menggunakan versi Log4J 2.17.2, sehingga untuk menampilkan flag kita harus gunakan cara lain.

- Potongan file `app.py` di bawah ini menggambarkan bahwa text yang diinputkan oleh user akan dikirimkan ke aplikasi Java dengan menggunakan `subprocess.run` dan hasil output serta **error-nya ditampilkan kembali kepada web**. Kita bisa berasumsi bahwa flag bisa didapatkan dengan pesan error.

```python
def start():
    if request.method == 'POST':
        text = request.form['text'].split(' ')
        cmd = ''
        if len(text) < 1:
            return ('invalid message', 400)
        elif len(text) < 2:
            cmd = text[0]
            text = ''
        else:
            cmd, text = text[0], ' '.join(text[1:])
        result = chat(cmd, text)
        return result
    return render_template('index.html')

def chat(cmd, text):
    # run java jar with a 10 second timeout
    res = subprocess.run(['java', '-jar', '-Dcmd=' + cmd, 'chatbot/target/app-1.0-SNAPSHOT.jar', '--', text], capture_output=True, timeout=10)
    print(res.stderr.decode('utf8'))
    return res.stdout.decode('utf-8')
```

- Potongan file `App.java` ini menggambarkan bahwa flag tersimpan pada environment variable. Baris code setelahnya hanya berkaitan dengan penanganan input user.
```java
public class App {
  public static Logger LOGGER = LogManager.getLogger(App.class);
  public static void main(String[]args) {
    String flag = System.getenv("FLAG");
    if (flag == null || !flag.startsWith("CTF")) {
        LOGGER.error("{}", "Contact admin");
    }
```

- Untuk melangkah lebih lanjut, kita perlu membaca dokumentasi lookup pada Log4j berikut:
	- Environment Lookup dan Java Lookup pada https://logging.apache.org/log4j/2.x/manual/lookups.html

- Kita bisa menginjeksikan % pada web tersebut dan menghasilkan error berikut.
![](attachments/Pasted%20image%2020220708113639.png)  

- Apabila kita menjalankan lookup versi java, justru yang didapatkan adalah seperti ini
![](attachments/Pasted%20image%2020220708114942.png)

- Hal ini diakibatkan oleh fungsi `chat` pada `app.py` yang mengembalikan `stdout`(hasil output yang berhasil dijalankan) dengan tetap melakukan print `stderr`(pesan error).
```python
def chat(cmd, text):
    # run java jar with a 10 second timeout
    res = subprocess.run(['java', '-jar', '-Dcmd=' + cmd, 'chatbot/target/app-1.0-SNAPSHOT.jar', '--', text], capture_output=True, timeout=10)
    print(res.stderr.decode('utf8'))
    return res.stdout.decode('utf-8')
```

- Yuk dapatkan flagnya dengan membuat pesan error dengan menambahkan environment lookup. PoC nya adalah apabila kita memasukkan `${java:abcd}`, maka terdapat pesan error berikut. `ERROR Resolver failed to lookup java:abcd`
![](attachments/Pasted%20image%2020220708115356.png)  

- Jadi, bagaimana jika kita melakukan double lookup yang menghasilkan error. `${java:${env:flag}}`

- Oopss...
![](attachments/Pasted%20image%2020220708115626.png)  

- Ini baru... `${java:${env:FLAG}}`
![](attachments/Pasted%20image%2020220708115711.png)

- Flag: CTF{d95528534d14dc6eb6aeb81c994ce8bd}
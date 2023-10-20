
создать .env в app с содержанием
```
SECRET_KEY=
MYSQL_HOST=mysql-headfirst
MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=
```

создать .env в database с содержанием
```
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=
```

создать скрипт для экспорта переменных среды, необходимых для развертывания set_make_env.sh
```bash
export MYSQL_ROOT_PASSWORD=
export MYSQL_DATABASE=
```
Все пересекающиеся переменные должны совпадать)

Далее в терминале в корневой директории:
Для первого запуска:
```bash
. ./set_make_env.sh
make init-run 
```
Для дампа базы(dump.sql положить в директорию /database/sql_scripts):
```bash
. ./set_make_env.sh
make dump-db
```
Для запуска приложения:
```bash
make run
```

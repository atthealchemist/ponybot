# ponybot
Requested ponybot for Nirton

## 1. Запуск бота и его сервисов
1. Для запуска проекта нам потребуюся Docker и git (обязательно)
Установить их можно следующим образом (Debian-based дистрибутивы)
```bash
sudo apt install docker-ce git
```
2. Подключаемся к серверу любым образом (telnet/ssh) и выполняем следующую команду:
```bash
git clone https://github.com/atthealchemist/ponybot.git -b alpha
```
где `-b alpha` - версия проекта, которую мы хотим запустить
3. Переходим в репозиторий с проектом
```bash
cd ponybot/
```
4. И выполняем следующую команду
```bash
docker-compose up --build -d
```

5. Если команда сработала как надо, то результат выполнения команды `docker-compose ps` должен выглядеть следующим образом:
```bash
(venv) ➜  ponybot git:(feature/setup_postgres) docker-compose ps
      Name                     Command               State                    Ports                  
-----------------------------------------------------------------------------------------------------
ponybot_db_1        docker-entrypoint.sh postgres    Up      0.0.0.0:5432->5432/tcp,:::5432->5432/tcp
ponybot_ponybot_1   ./docker-entrypoint.sh           Up      0.0.0.0:8000->8000/tcp,:::8000->8000/tcp
ponybot_redis_1     docker-entrypoint.sh redis ...   Up      6379/tcp      
```
Значения `Up` в колонке State символизируют о том, что сервисы успешно запущены и работают в фоновом режиме.

# Ponybot
Заказ на разработку понибота от 06.07.2021 года.
Версия: *alpha*

## Руководство по использованию системы

### 1. Запуск бота и его сервисов
1. Для запуска проекта нам потребуюся Docker и git (обязательно)
Установить их можно следующим образом (Debian-based дистрибутивы)
```bash
sudo apt install docker-ce git
```
2. Подключаемся к серверу любым образом (telnet/ssh) и выполняем следующую команду:
```bash
git clone https://github.com/atthealchemist/ponybot.git -b alpha
```
где `|b alpha` | версия проекта, которую мы хотим запустить
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
(server-HI4fhgSw-py3.8) ➜  server git:(alpha) docker-compose ps
         Name                       Command               State                 Ports               
----------------------------------------------------------------------------------------------------
ponybot-backend-server   ./entrypoint.sh server           Up      0.0.0.0:8000->8000/tcp,:::8000->80
                                                                  00/tcp                            
ponybot-bot              ./entrypoint.sh bot              Up                                        
ponybot-celery           ./entrypoint.sh celery           Up                                        
ponybot-celery-beat      ./entrypoint.sh celery-beat      Up                                        
ponybot-nginx            /docker-entrypoint.sh ngin ...   Up      0.0.0.0:80->80/tcp,:::80->80/tcp  
ponybot-postgres-db      docker-entrypoint.sh postgres    Up      0.0.0.0:5432->5432/tcp,:::5432->54
                                                                  32/tcp                            
ponybot-redis            docker-entrypoint.sh redis ...   Up      6379/tcp             
```
Значения `Up` в колонке **State** символизируют о том, что сервисы успешно запущены и работают в фоновом режиме.


## 2. Обслуживание системы
### Перезагрузка сервисов
Для того, чтобы перезагрузить сервис, введи
`docker-compose restart <service_name_1> <service_name_2> .. <service_name_N>`

| Имя контейнера         | Имя сервиса     |
|------------------------|-----------------|
| ponybot-backend-server | **server**      |
| ponybot-celery         | **celery**      |
| ponybot-celery-beat    | **celery-beat** |
| ponybot-nginx          | **nginx**       |
| ponybot-postgres-db    | **db**          |
| ponybot-redis          | **redis**       |

### Перезапуск бота
Для того, чтобы полностью перезапустить бота с нуля:
> #### Внимание! 
> Это действие полностью удаляет всю существующую информацию - пользователи, пони, подписки и т.д. -  из баз данных и redis!!!

```bash
docker-compose down
docker-compose up --build -d
```

### Просмотр логов сервиса
Для просмотра последних 20 строчек лога запущенного сервиса, введи
```bash
docker-compose logs -t <service_name> | tail -n 20
```

Для полного просмотра логов сервиса в интерактивном режиме, введи
```bash
docker-compose logs -t <service_name> | less -r
```

## 3. Администрирование системы
В системе доступна админка бота с суперпользователем (главным администратором)
`ponybot_dev_user` (пароль по умолчанию `!ponybot_dev_user!`)
Для входа в неё, зайди на сайт:
`<адрес_сервера>/admin/`


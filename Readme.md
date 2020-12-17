### Описание проекта

1. [Selenium](https://github.com/repen/csbet_selenium)
2. [Парсер](https://github.com/repen/csbetParser)
3. [Сайт](https://github.com/repen/csbetSite)


Установка

### Зависимости

Docker => [Docker install](https://docs.docker.com/engine/install/ubuntu/)

Запустить редис.

`docker run --name redisa --network=mynet --restart=always -d redis`


### Команды

1. Клонировать репо ```git clone https://github.com/repen/csbet_selenium.git```
2. Билд контейнера ```docker build -t selenium_docker .```
3. Запуск контейнера ```docker run --name csbet_selen -d -v csbet:/usr/src/app/data --network=mynet selenium_docker:latest```
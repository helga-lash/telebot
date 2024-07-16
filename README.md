# telebot
Telegram bot

## Submodule
* После клонирования репозитория необходимо клонировать подмодуль.
Для этого необходимо выполнить команды:
    ```bash
    git submodule init
    git submodule update
    ```
  * Подтянуть изменения из репозитория:
      ```bash
      cd helpers_entity/
      git fetch
      git merge origin/main
      cd ../
      ```

## Dev окружение:
* Запуск:
    ```bash
    docker compose -f docker-compose.yaml -f composes/dev.yaml up -d
    ```
* Остановка:
    ```bash
    docker compose -f docker-compose.yaml -f composes/dev.yaml down -v
    ```

## Тестирование релиза:
* Запуск:
    ```bash
    docker compose -f docker-compose.yaml -f composes/release.yaml up -d
    ```
* Остановка:
    ```bash
    docker compose -f docker-compose.yaml -f composes/release.yaml down -v
    ```
  
## Сборка контейнера:
```shell
docker build . --target prod --tag registry.xoma-net/lash_telebot:v0.2.0
```
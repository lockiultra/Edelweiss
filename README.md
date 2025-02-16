# Edelweiss

_Edelweiss_ — это пет-проект, представляющий собой микросервисную архитектуру, имитирующую работу, криптовалютного кошелька.

## Описание

Проект состоит из **трех** основных микросервисов:

- **Auth Service**  
  Отвечает за регистрацию и аутентификацию пользователей. При регистрации нового пользователя публикуется событие `user_registered` в RabbitMQ.

- **Wallet Service**  
  Управляет кошельками пользователей. После получения события о регистрации от Auth Service автоматически создаются кошельки для нового пользователя. Сервис также реализует операции по депозиту, снятию и переводу средств между кошельками.

  Дополнительно, для транзакций с токеном **Alpenglow** Wallet Service публикует сообщение в RabbitMQ, которое затем обрабатывается Blockchain Service.

- **Blockchain Service**  
  Имитирует работу простого блокчейна для внутреннего токена **Alpenglow**.  
  Сервис получает сообщения через RabbitMQ и записывает транзакции в цепочку блоков. Он предоставляет следующие эндпоинты:
  - **GET /** — проверка работоспособности сервиса.
  - **GET /chain** — получение текущей цепочки блоков.
  - **POST /add_transaction** — добавление транзакции (при условии, что валюта соответствует **Alpenglow**).

## Поддерживаемые токены

В кошельке можно хранить 6 типов токенов:
- **TON**
- **Bitcoin**
- **Ethereum**
- **Edilium** (утилити токен)
- **Alpenglow** (утилити токен)
- **Frostvyte** (утилити токен)

> **Примечание:** Логика работы и применения токенов находится в разработке. Транзакции с токеном **Alpenglow** дополнительно записываются в блокчейн через взаимодействие Wallet и Blockchain сервисов.

## Технологии

- **Python 3.12**
- **FastAPI**
- **SQLAlchemy 2.0**
- **PostgreSQL** (две базы данных: `edelweiss_auth` и `edelweiss_wallet`)
- **RabbitMQ**
- **JWT** для аутентификации
- **Docker & Docker Compose**

## Запуск проекта

Для сборки и запуска проекта используйте Docker Compose:

```bash
docker-compose up --build

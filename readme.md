# Проект "E-commerce с использованием Stripe"

## Описание проекта

Проект представляет собой простой интернет-магазин с интеграцией системы оплаты Stripe. Реализован с использованием Django и развернут в Docker-контейнерах.

## Установка

```bash
git clone https://github.com/Wandering-npc/simple_solutions.git
```
Создать файл .env по примеру с example
```bash
docker-compose up
```
Создайте суперюзера  
Перейдите по адресу http://localhost:8081/ для доступа к приложению.
## Использование
1. Получение сеанса оформления заказа для товара
GET /buy/<int:item_id>/
2. Просмотр подробной информации о товаре
GET /item/<int:item_id>/
3. Просмотр списка товаров
GET /items/
4. Добавление товара в корзину
GET /add_to_order/<int:item_id>/
5. Создание сессии оплаты
POST /create_payment_session/
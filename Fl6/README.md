
Сервер будет доступен по адресу http://localhost:8000.
Доступные запросы
1. Просмотр всех пользователей

GET http://localhost:8000/users/
Описание:
Получает список всех зарегистрированных пользователей.

2. Просмотр пользователя по ID
Запрос:
GET http://localhost:8000/users/{user_id}
Описание:
Получает информацию о пользователе по указанному ID.

Пример запроса:

http
Копировать код
GET http://localhost:8000/users/1
3. Создание нового пользователя
Запрос:

POST http://localhost:8000/users/
Тело запроса:

{
  "name": "John",
  "surname": "Doe",
  "email": "john.doe@example.com",
  "password": "securepassword"
}
Описание:
Создает нового пользователя с указанными данными.

4. Просмотр всех товаров
Запрос:

GET http://localhost:8000/products/
Описание:
Получает список всех доступных товаров.

5. Просмотр товара по ID
Запрос:

GET http://localhost:8000/products/{product_id}
Описание:
Получает информацию о товаре по указанному ID.

Пример запроса:

GET http://localhost:8000/products/1
6. Создание нового товара
Запрос:

POST http://localhost:8000/products/
Тело запроса:

{
  "name": "Sample Product",
  "description": "Description of the product.",
  "price": 19.99
}
Описание:
Создает новый товар с указанными данными.

7. Просмотр всех заказов
Запрос:

GET http://localhost:8000/orders/
Описание:
Получает список всех заказов.

8. Просмотр заказа по ID
Запрос:
GET http://localhost:8000/orders/{order_id}
Описание:
Получает информацию о заказе по указанному ID.

Пример запроса:

GET http://localhost:8000/orders/1
9. Создание нового заказа
Запрос:

POST http://localhost:8000/orders/
Тело запроса:

{
  "user_id": 1,
  "product_id": 1,
  "order_date": "2024-07-20",
  "status": "pending"
}
Описание:
Создает новый заказ с указанными данными.

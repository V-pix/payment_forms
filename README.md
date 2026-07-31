# Payment_forms - Сервер, который создает платёжные формы для товаров

## Оглавление
- [Описание проекта](#description)
- [Используемые технологии](#technologies)
- [Установка и запуск проекта](#launch)

<a id=description></a>
## Описание проекта
Сервер создает платёжные формы для товаров для имитации и тестирования платежей, с помощью платёжной системы Stripe. Проект был переработан на основе версии 2022 года: обновлены зависимости и структура, расширены модели товаров и заказов, добавлена проверка валюты, а работа со Stripe вынесена в отдельный сервисный модуль. 
Реализованы Django + Stripe API бэкенд со следующим функционалом:
- модель `Item` с названием, описанием, ценой, валютой и статусом активности;
- `GET /buy/{id}` — создание Stripe Checkout Session для выбранного товара и получение `session.id`;
- `GET /item/{id}` — HTML-страница товара с кнопкой `Buy` и переходом к оплате через Stripe Checkout;
- каталог активных товаров;
- сессионная корзина с добавлением, удалением товаров и расчётом общей стоимости;
- модели `Order` и `OrderItem` для оформления заказа из нескольких товаров;
- создание одной Stripe Checkout Session для оплаты всего заказа;
- отдельный сервисный модуль для работы со Stripe;
- управление товарами и заказами через Django Admin;
- хранение настроек и ключей в environment variables (специально выгружены на github для тестирования);
- запуск проекта через Docker.

---
<a id=technologies></a>
## Используемые технологии:
- Python 3.12
- Django 5.2
- Stripe Python 15.3
- Docker

<a id=launch></a>
## Установка и запуск проекта с Docker
### 1. Клонировать репозиторий
```bash
git clone git@github.com:V-pix/payment_forms.git
```
### 2. Перейти в репозиторий в командной строке:
```bash
cd payment_forms
```
### 3. Установить `docker` и `docker-compose`, если они не установлены:
```bash
https://docs.docker.com/get-docker/
```
```bash
https://docs.docker.com/compose/
```
### 4. Cоберите контейнер и запустите:
```bash
docker build -t payment_forms .
```
```bash
docker-compose up -d
```
### Выполните миграции:
```bash
docker-compose exec web python manage.py migrate
```
### Заполните тестовые данные:
```bash
docker-compose exec web python manage.py loaddata dump.json
```

### Теперь проект доступен по адресам:
http://localhost:8000/ 

http://localhost:8000/admin/

http://localhost:8000/item/1/

http://localhost:8000/buy/1/

### Учетная запись администратора
```sh
login: admin
password: 123
```
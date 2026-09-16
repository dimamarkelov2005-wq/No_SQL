# Лабораторная работа №3: Выполнение операций Insert, Find, Update и Delete в MongoDB

* **Дисциплина:** Нереляционные базы данных (NoSQL)
* **Вариант:** №2 (Интернет-магазин)
* **База данных:** `shopDB`
* **Коллекция:** `products`
* **Среда выполнения:** MongoDB Compass / mongosh

---

## 1. Цель работы
Освоить практический цикл операций CRUD (Create, Read, Update, Delete) в MongoDB. Научиться работать с BSON-типами, фильтрацией, операторами сравнения, вложенными документами (dot notation), массивами, проекцией, сортировкой и точечным изменением/удалением документов.

---

## 2. Структура документа
Каждый документ коллекции `products` содержит следующие обязательные поля:
* `productId` (Number) — уникальный идентификатор товара;
* `name` (String) — наименование товара;
* `brand` (String) — бренд;
* `price` (Number) — цена;
* `stock` (Number) — остаток на складе;
* `rating` (Number) — рейтинг товара;
* `active` (Boolean) — доступность для продажи;
* `tags` (Array) — список категорий/тегов;
* `specifications` (Object) — вложенный объект с техническими характеристиками.

---

## 3. Ход выполнения и основные команды
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/103786b7-15fd-4ebc-a0c0-01d3639d92be" />


### Вставка данных (INSERT)
Добавлен одиночный документ и массив из 9 документов для выполнения требования (не менее 10 исходных записей):

```javascript
db.products.insertOne({
  productId: 101, name: "Laptop Pro 15", brand: "TechCorp", price: 1200, stock: 15, rating: 4.8, active: true,
  tags: ["electronics", "laptops", "bestseller"],
  specifications: { ram: "16GB", storage: "512GB SSD", color: "Space Gray" }
});

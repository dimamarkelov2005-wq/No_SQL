// Переключаемся на базу данных лабораторной работы
use university_lab10;

// Вставка тестовых документов с подтверждением записи большинством узлов
db.orders.insertMany([
  { item: "cardboard", qty: 25, status: "A" },
  { item: "paper", qty: 100, status: "B" },
  { item: "planner", qty: 75, status: "A" }
  // ... сюда можно добавить остальные документы
], { 
  writeConcern: { w: "majority", wtimeout: 5000 } 
});

print("Данные успешно добавлены!");

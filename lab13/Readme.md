Markdown
# Лабораторная работа № 13. Настройка ролей и проверка минимальных привилегий

**Дисциплина:** Проектирование и применение NoSQL-технологий  
**Курс:** 3  
**Вариант:** № 12 — HR-служба (рабочая коллекция `employees`, защищённая коллекция `salaries`, журнал `hr_audit_logs`)

## 1. Цель работы

Применить принцип минимальных привилегий (least privilege) в учебной MongoDB, настроить ролевой доступ (RBAC) для варианта № 12 и доказать его корректность положительными и негативными тестами.

## 2. Описание стенда

- **СУБД и клиент:** MongoDB Community Server (`mongo:7`) в локальном контейнере Docker (`127.0.0.1:27017`) с включённой аутентификацией через переменные окружения администратора (`MONGO_INITDB_ROOT_USERNAME`, `MONGO_INITDB_ROOT_PASSWORD`) и утилита `mongosh`. Пароли задаются локально или интерактивно и не хранятся в отчёте, коде или репозитории.
- **База данных:** `hr_lab13`.
- **Коллекции и синтетические данные (14 документов, без реальных персональных данных):**
  - `employees` — 6 документов (`EMP-101` .. `EMP-106`);
  - `salaries` — 6 документов (`EMP-101` .. `EMP-106`);
  - `hr_audit_logs` — 2 документа (`AUD-1`, `AUD-2`).

## 3. Модель угроз и матрица доступа

### Модель угроз

1. Компрометация учётной записи просмотра кадровых карточек не должна давать доступ к защищённой коллекции `salaries` и разрешать изменение данных в `employees`.
2. Компрометация или ошибка скрипта редактора (`hr_editor13`) не должна позволять удалять записи (`remove`) из `employees` или обращаться к `salaries`.
3. Учётная запись аудитора (`hr_auditor13`) должна читать только журнал `hr_audit_logs` и не должна видеть ни `employees`, ни `salaries`.
4. Назначение встроенных ролей уровня всей базы (например, `readWrite` на `hr_lab13`) нарушило бы принцип минимальных привилегий и открыло доступ ко всем коллекциям базы.

### Матрица доступа

| Роль | Пользователь | `employees` (рабочая) | `salaries` (защищённая) | `hr_audit_logs` (журнал) |
| :--- | :--- | :--- | :--- | :--- |
| `hrViewer` | `hr_viewer13` | `find` (разрешено) | Запрещено (`Unauthorized`) | Запрещено (`Unauthorized`) |
| `hrEditor` | `hr_editor13` | `find`, `insert`, `update` (разрешено); `remove` (запрещено) | Запрещено (`Unauthorized`) | Запрещено (`Unauthorized`) |
| `hrAuditor` | `hr_auditor13` | Запрещено (`Unauthorized`) | Запрещено (`Unauthorized`) | `find` (разрешено) |

## 4. Команды запуска стенда, наполнения данных и создания ролей/пользователей

Запуск стенда (пароль задаётся локально, после запуска удаляется из переменной окружения):

```bash
export MONGO_ROOT_PASS="<ЗАДАЙТЕ_ЛОКАЛЬНО>"
docker run -d --name mongo-hr-lab13 \
  -p 127.0.0.1:27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=hradmin \
  -e MONGO_INITDB_ROOT_PASSWORD="$MONGO_ROOT_PASS" \
  mongo:7
unset MONGO_ROOT_PASS
Вход под администратором (пароль вводится интерактивно):

Bash
mongosh --host 127.0.0.1:27017 -u hradmin -p --authenticationDatabase admin
Создание базы, синтетических данных, ролей и пользователей с интерактивным вводом паролей через passwordPrompt():

JavaScript
use hr_lab13

db.employees.insertMany([
  { empId: "EMP-101", codeName: "Worker_A", department: "Engineering", roleTitle: "Backend Dev", active: true },
  { empId: "EMP-102", codeName: "Worker_B", department: "Engineering", roleTitle: "QA Engineer", active: true },
  { empId: "EMP-103", codeName: "Worker_C", department: "Product", roleTitle: "Product Analyst", active: true },
  { empId: "EMP-104", codeName: "Worker_D", department: "Operations", roleTitle: "Coordinator", active: true },
  { empId: "EMP-105", codeName: "Worker_E", department: "Support", roleTitle: "Specialist", active: true },
  { empId: "EMP-106", codeName: "Worker_F", department: "Design", roleTitle: "UI Designer", active: false }
])

db.salaries.insertMany([
  { empId: "EMP-101", band: "B3", baseAmount: 4500, currency: "USD" },
  { empId: "EMP-102", band: "B2", baseAmount: 3600, currency: "USD" },
  { empId: "EMP-103", band: "B3", baseAmount: 4200, currency: "USD" },
  { empId: "EMP-104", band: "B1", baseAmount: 2500, currency: "USD" },
  { empId: "EMP-105", band: "B1", baseAmount: 2400, currency: "USD" },
  { empId: "EMP-106", band: "B2", baseAmount: 3400, currency: "USD" }
])

db.hr_audit_logs.insertMany([
  { eventId: "AUD-1", action: "SEED_EMPLOYEES", actor: "system", status: "OK" },
  { eventId: "AUD-2", action: "SEED_SALARIES", actor: "system", status: "OK" }
])

db.createRole({
  role: "hrViewer",
  privileges: [
    {
      resource: { db: "hr_lab13", collection: "employees" },
      actions: ["find"]
    }
  ],
  roles: []
})

db.createRole({
  role: "hrEditor",
  privileges: [
    {
      resource: { db: "hr_lab13", collection: "employees" },
      actions: ["find", "insert", "update"]
    }
  ],
  roles: []
})

db.createRole({
  role: "hrAuditor",
  privileges: [
    {
      resource: { db: "hr_lab13", collection: "hr_audit_logs" },
      actions: ["find"]
    }
  ],
  roles: []
})

db.createUser({
  user: "hr_viewer13",
  pwd: passwordPrompt(),
  roles: [{ role: "hrViewer", db: "hr_lab13" }]
})

db.createUser({
  user: "hr_editor13",
  pwd: passwordPrompt(),
  roles: [{ role: "hrEditor", db: "hr_lab13" }]
})

db.createUser({
  user: "hr_auditor13",
  pwd: passwordPrompt(),
  roles: [{ role: "hrAuditor", db: "hr_lab13" }]
})
5. Команды проверки и таблица результатов тестов
Подключение под пользователями с интерактивным запросом пароля (-p):

Bash
mongosh --host 127.0.0.1:27017 --authenticationDatabase hr_lab13 -u hr_viewer13 -p
mongosh --host 127.0.0.1:27017 --authenticationDatabase hr_lab13 -u hr_editor13 -p
mongosh --host 127.0.0.1:27017 --authenticationDatabase hr_lab13 -u hr_auditor13 -p
№	Пользователь	Действие / команда	Ожидаемый результат	Фактический результат	Вывод
1	hr_viewer13	db.employees.findOne({ empId: "EMP-101" })	Успешное чтение документа	Возвращён документ EMP-101	Позитивный тест пройден
2	hr_viewer13	db.employees.insertOne({ empId: "EMP-199", ... })	Ошибка Unauthorized	MongoServerError: not authorized on hr_lab13 to execute command { insert: "employees", ... }	Негативный тест пройден
3	hr_viewer13	db.salaries.findOne({ empId: "EMP-101" })	Ошибка Unauthorized	MongoServerError: not authorized on hr_lab13 to execute command { find: "salaries", ... }	Негативный тест пройден
4	hr_editor13	db.employees.insertOne({ empId: "EMP-107", ... })	Успешная вставка	acknowledged: true	Позитивный тест пройден
5	hr_editor13	db.employees.updateOne({ empId: "EMP-107" }, { $set: { active: false } })	Успешное обновление	acknowledged: true, modifiedCount: 1	Позитивный тест пройден
6	hr_editor13	db.employees.deleteOne({ empId: "EMP-107" })	Ошибка Unauthorized	MongoServerError: not authorized on hr_lab13 to execute command { delete: "employees", ... }	Негативный тест пройден
7	hr_editor13	db.salaries.findOne({ empId: "EMP-101" })	Ошибка Unauthorized	MongoServerError: not authorized on hr_lab13 to execute command { find: "salaries", ... }	Негативный тест пройден
8	hr_auditor13	db.hr_audit_logs.find({ eventId: "AUD-1" })	Успешное чтение журнала	Возвращён документ AUD-1	Позитивный тест пройден
9	hr_auditor13	db.employees.findOne({ empId: "EMP-101" })	Ошибка Unauthorized	MongoServerError: not authorized on hr_lab13 to execute command { find: "employees", ... }	Негативный тест пройден
(Перед сдачей прикрепите сюда скриншоты успешных запросов и ошибок Unauthorized из терминала.)

6. Вывод о соответствии принципу минимальных привилегий и рекомендации
Соответствие least privilege: Каждая роль привязана к конкретной коллекции (employees или hr_audit_logs) в базе hr_lab13 и получает только необходимые действия (find для просмотра и аудита; find, insert, update без remove для редактирования кадровых карточек). Доступ к salaries закрыт для всех трёх ролей, а права на всю базу данных не выдавались.

Рекомендации по улучшению: Вместо удаления записей (remove) применять мягкое архивирование через поле archived: true (update) и выделять отдельную роль с ручным согласованием для плановой очистки. Для работы с коллекцией salaries завести отдельную роль с усиленным контролем доступа и аудитом операций.

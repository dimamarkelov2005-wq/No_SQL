// --- 1. Подключиться как hr_viewer13 (--authenticationDatabase hr_lab13 -u hr_viewer13 -p) ---
use hr_lab13
db.employees.findOne({ empId: "EMP-101" }) // Ожидается: документ EMP-101
db.employees.insertOne({ empId: "EMP-199", codeName: "Test_X", department: "HR", roleTitle: "Intern", active: true }) // Ожидается: Unauthorized
db.salaries.findOne({ empId: "EMP-101" }) // Ожидается: Unauthorized

// --- 2. Подключиться как hr_editor13 (--authenticationDatabase hr_lab13 -u hr_editor13 -p) ---
use hr_lab13
db.employees.insertOne({ empId: "EMP-107", codeName: "Worker_G", department: "HR", roleTitle: "Recruiter", active: true }) // Ожидается: acknowledged: true
db.employees.updateOne({ empId: "EMP-107" }, { $set: { active: false } }) // Ожидается: acknowledged: true
db.employees.deleteOne({ empId: "EMP-107" }) // Ожидается: Unauthorized
db.salaries.findOne({ empId: "EMP-101" }) // Ожидается: Unauthorized

// --- 3. Подключиться как hr_auditor13 (--authenticationDatabase hr_lab13 -u hr_auditor13 -p) ---
use hr_lab13
db.hr_audit_logs.find({ eventId: "AUD-1" }) // Ожидается: документ AUD-1
db.employees.findOne({ empId: "EMP-101" }) // Ожидается: Unauthorized

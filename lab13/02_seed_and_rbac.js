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

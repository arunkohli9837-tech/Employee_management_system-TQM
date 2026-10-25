-- Employee Management System
-- Initial SQLite database schema


CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
        CHECK (role IN ('Admin', 'HR', 'Employee')),
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    employee_code TEXT NOT NULL UNIQUE COLLATE NOCASE,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE COLLATE NOCASE,
    phone TEXT NOT NULL,
    department TEXT NOT NULL,
    designation TEXT NOT NULL,
    salary REAL NOT NULL
        CHECK (salary >= 0),
    joining_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Active'
        CHECK (status IN ('Active', 'Inactive')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    username TEXT,
    action TEXT NOT NULL,
    target_type TEXT,
    target_id INTEGER,
    description TEXT,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS error_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    error_type TEXT NOT NULL,
    message TEXT NOT NULL,
    module TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS backup_history (
    id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL
        CHECK (operation IN ('Backup', 'Restore')),
    file_path TEXT NOT NULL,
    status TEXT NOT NULL,
    initiated_by INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    FOREIGN KEY (initiated_by)
        REFERENCES users(id)
        ON DELETE SET NULL
);

-- Payroll records are stored per employee and pay period. This project uses
-- simple monthly salary figures; statutory tax/benefit calculations are out of scope.
CREATE TABLE IF NOT EXISTS payroll_records (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    pay_period TEXT NOT NULL,
    basic_salary REAL NOT NULL CHECK (basic_salary >= 0),
    deductions REAL NOT NULL DEFAULT 0 CHECK (deductions >= 0),
    bonus REAL NOT NULL DEFAULT 0 CHECK (bonus >= 0),
    net_salary REAL NOT NULL CHECK (net_salary >= 0),
    created_by INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (employee_id, pay_period),
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    CHECK (net_salary >= 0)
);

CREATE TABLE IF NOT EXISTS performance_logs (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    review_date TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comments TEXT NOT NULL CHECK (length(trim(comments)) > 0),
    created_by INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS profiles (
    id SERIAL PRIMARY KEY,
    txid VARCHAR(500) NOT NULL,
    main_value TEXT,
    step_index INTEGER,
    start_time INTEGER,
    start_cpu INTEGER,
    elapsed INTEGER,
    cputime INTEGER,
    step_type INTEGER,
    step_order INTEGER,
    step_type_name VARCHAR(64),
    param TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

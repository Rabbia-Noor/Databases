USE school_mysql;

CREATE TABLE environment_info (
    marker_key VARCHAR(30) PRIMARY KEY,
    environment VARCHAR(10) NOT NULL
);
INSERT INTO environment_info VALUES ('environment', 'dev');

CREATE TABLE students (
    roll_no VARCHAR(30) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
INSERT INTO students VALUES ('SEED-MYSQL', 'MySQL Seed Student');

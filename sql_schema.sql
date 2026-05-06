-- SQL Schema for PhonePe Pulse Data

CREATE DATABASE IF NOT EXISTS phonepe_pulse;
USE phonepe_pulse;

-- 1. Aggregated Transaction
CREATE TABLE IF NOT EXISTS Aggregated_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(255),
    Year INT,
    Quarter INT,
    transaction_type VARCHAR(255),
    transaction_count BIGINT,
    transaction_amount DOUBLE
);

-- 2. Aggregated User
CREATE TABLE IF NOT EXISTS Aggregated_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(255),
    Year INT,
    Quarter INT,
    brand VARCHAR(255),
    user_count BIGINT,
    user_percentage DOUBLE
);

-- 3. Aggregated Insurance
CREATE TABLE IF NOT EXISTS Aggregated_insurance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(255),
    Year INT,
    Quarter INT,
    insurance_type VARCHAR(255),
    insurance_count BIGINT,
    insurance_amount DOUBLE
);

-- 4. Map Transaction
CREATE TABLE IF NOT EXISTS Map_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(255),
    Year INT,
    Quarter INT,
    district VARCHAR(255),
    transaction_count BIGINT,
    transaction_amount DOUBLE
);

-- 5. Map User
CREATE TABLE IF NOT EXISTS Map_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(255),
    Year INT,
    Quarter INT,
    district VARCHAR(255),
    registered_users BIGINT,
    app_opens BIGINT
);

-- 6. Map Insurance
CREATE TABLE IF NOT EXISTS Map_insurance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(255),
    Year INT,
    Quarter INT,
    district VARCHAR(255),
    insurance_count BIGINT,
    insurance_amount DOUBLE
);

-- 7. Top Transaction
CREATE TABLE IF NOT EXISTS Top_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(255),
    Year INT,
    Quarter INT,
    entity_type VARCHAR(50), -- 'district' or 'pincode'
    entity_name VARCHAR(255),
    transaction_count BIGINT,
    transaction_amount DOUBLE
);

-- 8. Top User
CREATE TABLE IF NOT EXISTS Top_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(255),
    Year INT,
    Quarter INT,
    entity_type VARCHAR(50), -- 'district' or 'pincode'
    entity_name VARCHAR(255),
    registered_users BIGINT
);

-- 9. Top Insurance
CREATE TABLE IF NOT EXISTS Top_insurance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(255),
    Year INT,
    Quarter INT,
    entity_type VARCHAR(50), -- 'district' or 'pincode'
    entity_name VARCHAR(255),
    insurance_count BIGINT,
    insurance_amount DOUBLE
);

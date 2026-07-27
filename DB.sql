DROP TABLE api_status;
CREATE TABLE api_status (
id INT AUTO_INCREMENT PRIMARY KEY,
page_name VARCHAR(255),
api_url TEXT,
status_code INT,
priority VARCHAR(10),
action VARCHAR(50),
response_time FLOAT,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SHOW TABLES;
DESCRIBE api_status;

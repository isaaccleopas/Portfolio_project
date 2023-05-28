-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS event_test_db;
CREATE USER IF NOT EXISTS 'event_test'@'localhost' IDENTIFIED BY 'event_test_pwd';
GRANT ALL PRIVILEGES ON `event_test_db`.* TO 'event_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'event_test'@'localhost';
FLUSH PRIVILEGES;

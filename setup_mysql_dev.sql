-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS event_dev_db;
CREATE USER IF NOT EXISTS 'event_dev'@'localhost' IDENTIFIED BY 'event_dev_pwd';
GRANT ALL PRIVILEGES ON `event_dev_db`.* TO 'event_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'event_dev'@'localhost';
FLUSH PRIVILEGES;

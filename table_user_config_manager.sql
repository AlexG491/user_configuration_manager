CREATE DATABASE IF NOT EXISTS user_config_manager;

USE user_config_manager;

CREATE TABLE IF NOT EXISTS settings(
  id INT NOT NULL AUTO_INCREMENT,
  setting_name varchar(100) NOT NULL,
  setting_value varchar(100) NOT NULL,
  PRIMARY KEY(id),
  UNIQUE (setting_name)
);


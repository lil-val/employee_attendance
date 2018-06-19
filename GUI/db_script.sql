CREATE DATABASE `attendance` /*!40100 DEFAULT CHARACTER SET utf8 */;

CREATE TABLE `employees` (
  `employee_id` CHAR(6) NOT NULL,
  `name` varchar(45) NOT NULL,
  `age` int(11) NOT NULL,
  `phone` varchar(10) NOT NULL,
  PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `employees_attendance` (
  `record_id` int(11) NOT NULL AUTO_INCREMENT,
  `employee_id` int(11) NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`record_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

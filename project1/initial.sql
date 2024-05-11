DROP TABLE IF EXISTS `departments`;
DROP TABLE IF EXISTS `sections`;
DROP TABLE IF EXISTS `q_and_a_pairs`;

CREATE TABLE IF NOT EXISTS `departments` (
    `department_id` TEXT,
    `print_name` TEXT NOT NULL,
  	PRIMARY KEY (`department_id`)
);

CREATE TABLE IF NOT EXISTS `sections` (
    `section_id` TEXT,
    `print_name` TEXT NOT NULL,
    `department_id` TEXT NOT NULL,
  	PRIMARY KEY (`section_id`)
);

CREATE TABLE IF NOT EXISTS `q_and_a_pairs` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT, 
    `question` TEXT NOT NULL, 
    `answer` TEXT NOT NULL,
    `section_id` TEXT NOT NULL
);
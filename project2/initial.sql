DROP TABLE IF EXISTS `teachers`;
DROP TABLE IF EXISTS `subjects`;
DROP TABLE IF EXISTS `subject_times`;
DROP TABLE IF EXISTS `site_class_tables`;

CREATE TABLE IF NOT EXISTS `teachers` (
    `name` TEXT,
    PRIMARY KEY (`name`)
);

CREATE TABLE IF NOT EXISTS `subjects` (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    teacher TEXT FORIEGN KEY REFERENCES teachers(`name`)
    -- TODO
);

CREATE TABLE IF NOT EXISTS `subject_times` (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    subject_id INTEGER FORIEGN KEY REFERENCES subjects(id),
    `day` TEXT NOT NULL, 
    `section` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `site_class_tables` (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    `source` TEXT NOT NULL
);
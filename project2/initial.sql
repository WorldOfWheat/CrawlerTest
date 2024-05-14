DROP TABLE IF EXISTS `subjects`;

CREATE TABLE IF NOT EXISTS `subjects` (
    id TEXT NOT NULL PRIMARY KEY, -- 課程代碼 
    subject_name TEXT NOT NULL, -- 科目名稱
    subject_eng_name TEXT NOT NULL, -- 科目英文名稱
    credit REAL NOT NULL, -- 學分
    teacher_name TEXT NOT NULL, -- 老師名稱
    `required` INTEGER NOT NULL, -- 必修/選修
    `day` TEXT NOT NULL, -- 上課日
    `sections` TEXT NOT NULL -- 上課節次
    `classroom` TEXT NOT NULL -- 上課教室
);
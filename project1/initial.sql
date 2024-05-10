DROP TABLE IF EXISTS `sections`;
DROP TABLE IF EXISTS `q_and_a_pairs`;

CREATE TABLE IF NOT EXISTS `sections` (
    section_id TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS `q_and_a_pairs` (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    section_id TEXT FORIEGN KEY REFERENCES sections(section_id),
    question TEXT NOT NULL, 
    answer TEXT NOT NULL
);
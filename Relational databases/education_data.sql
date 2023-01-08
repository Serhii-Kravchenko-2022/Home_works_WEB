-- Table: student
DROP TABLE IF EXISTS student;
CREATE TABLE student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL
);

-- Table: class
DROP TABLE IF EXISTS class;
CREATE TABLE class (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(3) UNIQUE NOT NULL
);

-- Table: teacher
DROP TABLE IF EXISTS teacher;
CREATE TABLE teacher (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL
);

-- Table: subject
DROP TABLE IF EXISTS subject;
CREATE TABLE subject (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(20) UNIQUE NOT NULL,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teacher (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

-- Table: grade
DROP TABLE IF EXISTS grade;
CREATE TABLE grade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_id INTEGER,
    value INT NOT NULL,
    data DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subject (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);
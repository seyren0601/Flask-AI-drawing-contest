DROP DATABASE IF EXISTS ai_drawing_contest;
CREATE DATABASE ai_drawing_contest;
USE ai_drawing_contest;

CREATE TABLE user(
	user_id int auto_increment,
    name nvarchar(256),
    email nvarchar(256),
    phone_number nvarchar(256),
    group_id tinyint,
    salt nvarchar(128),
    hashed_pw nvarchar(256),
    session_token text,
    address text,
    date_of_birth date,
    register_date date,
    school varchar(128),
    grade smallint,
    PRIMARY KEY(user_id)
);

INSERT INTO user(name, email, group_id)
VALUES 
	("Thịnh Nguyễn", "sorrenw@gmail.com", 0),
    ("abc", "abc@gmail.comm", 3)

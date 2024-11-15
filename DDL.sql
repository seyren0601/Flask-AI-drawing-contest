USE ai_drawing_contest;

CREATE TABLE user(
	user_id int auto_increment,
    name nvarchar(256),
    email nvarchar(256),
    phone_number nvarchar(256),
    group_id tinyint,
    salt nvarchar(128),
    hashed_pw nvarchar(256),
    session_token text
);

CREATE TABLE participant(
	user_id int,
    address text,
    date_of_birth date,
    register_date date,
    school varchar(128),
    grade smallint
);
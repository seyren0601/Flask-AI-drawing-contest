DROP DATABASE IF EXISTS ai_drawing_contest;
CREATE DATABASE ai_drawing_contest;
USE ai_drawing_contest;

CREATE TABLE user(
	user_id int auto_increment,
    name nvarchar(256),
    username nvarchar(128),
    email nvarchar(256),
    phone_number nvarchar(256),
    group_id tinyint,
    salt nvarchar(128),
    hashed_pw nvarchar(256),
    session_token text,
    register_date date,
    PRIMARY KEY(user_id)
);

CREATE TABLE prompts(
    prompt_id int auto_increment,
    team_id int,
    date_time datetime,
    prompt LONGTEXT,
    image LONGTEXT,
    submitted boolean,
    PRIMARY KEY(prompt_id),
    FOREIGN KEY (team_id) REFERENCES user(user_id)
);

INSERT INTO user(username, name, email, group_id)
VALUES
	("adm0001", "Thịnh Nguyễn", "sorrenw@gmail.com", 0),
    ("usr0000", "team_name", "abc@gmail.comm", 3);
    
INSERT INTO prompts(team_id, prompt, image, submitted)
VALUES
	(1, "abc", "b64", 0)
DROP DATABASE IF EXISTS ai_drawing_contest;
CREATE DATABASE ai_drawing_contest;
USE ai_drawing_contest;

CREATE TABLE team(
	team_id int auto_increment,
    team_name nvarchar(128),
    create_date date,
    PRIMARY KEY(team_id)
);

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
    address text,
    date_of_birth date,
    register_date date,
    school varchar(128),
    grade smallint,
    team_id integer,
    team_leader boolean,
    PRIMARY KEY(user_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id)
);

CREATE TABLE prompts(
    prompt_id int auto_increment,
    team_id int,
    date_time datetime,
    prompt LONGTEXT,
    image LONGTEXT,
    submitted boolean,
    PRIMARY KEY(prompt_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id)
);


INSERT INTO team(team_name, create_date) 
VALUES("lmao", "2024-11-15");

INSERT INTO user(username, name, email, group_id, team_leader, team_id)
VALUES
	("adm0001", "Thịnh Nguyễn", "sorrenw@gmail.com", 0, false, null),
    ("usr0000", "abc", "abc@gmail.comm", 3, true, 1);
    
INSERT INTO prompts(team_id, prompt, image, submitted)
VALUES
	(1, "abc", "b64", 0)
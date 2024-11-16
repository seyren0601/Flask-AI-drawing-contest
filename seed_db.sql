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

CREATE TABLE submission(
	submission_id int auto_increment,
    prompt_id int,
    submit_date datetime,
    video varchar(256),
    score float,
    PRIMARY KEY(submission_id),
    FOREIGN KEY(prompt_id) REFERENCES prompts(prompt_id)
);

INSERT INTO user(username, name, email, group_id)
VALUES
	("adm0001", "Thịnh Nguyễn", "sorrenw@gmail.com", 0),
    ("usr00000", "team_name", "abc@gmail.com", 3),
    ("usr00001", "team_name", "xyz@gmail.com", 3);
    
INSERT INTO prompts(team_id, prompt, image, submitted)
VALUES
	(2, "abc", "b64", 0),
    (2, "xyz", "b64", 0),
    (2, "qwerty", "b64", 0),
    (3, "abc", "b64", 0),
    (3, "xyz", "b64", 0),
    (3, "qwerty", "b64", 0);

/*INSERT INTO submission(prompt_id, video)
VALUES
	(1, "sample_url"),
    (5, "sample_url");*/
    
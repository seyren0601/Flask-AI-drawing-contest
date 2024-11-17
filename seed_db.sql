DROP DATABASE IF EXISTS ai_drawing_contest;
CREATE DATABASE ai_drawing_contest;
USE ai_drawing_contest;

CREATE TABLE user(
	user_id int auto_increment,
    name nvarchar(256),
    username nvarchar(128) unique,
    email nvarchar(256),
    phone_number nvarchar(256),
    group_id tinyint,
    salt nvarchar(128),
    hashed_pw nvarchar(256),
    session_token text,
    register_date date,
    team_info text,
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

CREATE TABLE assigned_submissions(
	grader_id int ,
    submission_id int,
    assigner_id int,
    status smallint,
    modified_date datetime,
    comment text,
    assigned_date datetime,
    PRIMARY KEY(grader_id,submission_id),
    FOREIGN KEY(grader_id) REFERENCES user(user_id),
    FOREIGN KEY(submission_id) REFERENCES submission(submission_id),
    FOREIGN KEY(assigner_id) REFERENCES user(user_id)
);

INSERT INTO user(username, name, email, group_id)
VALUES
	("adm00001", "Thịnh Nguyễn", "sorrenw@gmail.com", 0),
    ("usr00002", "abcxyz", "aaa@gmail.com", 2),
    ("usr00003", "asdfas", "asw@gmail.com", 1),
	("usr00004", "wqtah", "aaa@gmail.com", 2),
    ("usr00005", "qwetasd", "aaa@gmail.com", 1);
    
INSERT INTO prompts(team_id, prompt, image, submitted)
VALUES
	(2, "abc", "b64", 0),
    (2, "xyz", "b64", 0),
    (2, "qwerty", "b64", 0),
    (3, "abc", "b64", 0),
    (3, "xyz", "b64", 0),
    (3, "qwerty", "b64", 0);

INSERT INTO submission(prompt_id, video)
VALUES
	(1, "sample_url"),
    (5, "sample_url");

INSERT INTO assigned_submissions(grader_id, assigner_id, submission_id, status, modified_date, assigned_date)
VALUES
	(2, 3, 1, 0, "2024-11-16", "2024-11-16"),
    (4, 5, 2, 0, "2024-11-16", "2024-11-16");

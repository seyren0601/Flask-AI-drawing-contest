DROP DATABASE IF EXISTS ai_drawing_contest;
CREATE DATABASE ai_drawing_contest;
USE ai_drawing_contest;

CREATE TABLE user(
	user_id int auto_increment,
    name nvarchar(256),
    username nvarchar(128) unique,
    school_name nvarchar(256),
    grade nvarchar(256),
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
    FOREIGN KEY (team_id) REFERENCES user(user_id) ON DELETE CASCADE
);

CREATE TABLE submission(
	submission_id int auto_increment,
    prompt_id int,
    submit_date datetime,   
    assigned boolean,
    PRIMARY KEY(submission_id),
    FOREIGN KEY(prompt_id) REFERENCES prompts(prompt_id) ON DELETE CASCADE
);

CREATE TABLE assigned_submissions(
    submission_id int,
    img_grader_id int,    
    prompt_grader_id int,
    img_comment text,    
    prompt_comment text,
    img_score float,    
    prompt_score float,
    status boolean,
    modified_date datetime,
    PRIMARY KEY(submission_id, img_grader_id, prompt_grader_id),
    FOREIGN KEY(submission_id) REFERENCES submission(submission_id) ON DELETE CASCADE,
	FOREIGN KEY(img_grader_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY(prompt_grader_id) REFERENCES user(user_id) ON DELETE CASCADE
);

INSERT INTO user(username, name, email, group_id)
VALUES
	("usr00000", "Thịnh Nguyễn", "sorrenw@gmail.com", 0),
    ("usr00001", "team_1", "aaa@gmail.com", 2),
    ("usr00002", "grader_1", "asw@gmail.com", 1),
	("usr00003", "team_2", "aaa@gmail.com", 2),
    ("usr00004", "grader_2", "aaa@gmail.com", 1),
    ("usr00005", "grader_3", "aaa@gmail.com", 1);
    
INSERT INTO user(username, name, group_id, salt, hashed_pw)
VALUES("usr00006", "team_3", 2, "$2b$12$BZyS/bsY816Aw5tZADVMLe", "$2b$12$BZyS/bsY816Aw5tZADVMLeSGEklXB2346NneyjXEPN/CcRXjcslou");
    
INSERT INTO prompts(team_id, prompt, image, submitted)
VALUES
	(2, "abc", "b64", 1),
    (2, "xyz", "b64", 0),
    (2, "qwerty", "b64", 0),
    (4, "abc", "b64", 0),
    (4, "xyz", "b64", 1),
    (4, "qwerty", "b64", 0);

INSERT INTO submission(prompt_id, assigned)
VALUES
	(1,  0),
    (5,  0);

-- INSERT INTO submission(prompt_id, assigned)
-- VALUES
-- 	(1, 1),
--     (5,1);

INSERT INTO assigned_submissions(submission_id, img_grader_id, prompt_grader_id, status)
VALUES
	(1, 3,  6, 0),
    (2, 3,5, 0);
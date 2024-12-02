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

CREATE TABLE submission(
	submission_id int auto_increment,
    submit_date datetime,
    assigned boolean,
    PRIMARY KEY(submission_id)
);

CREATE TABLE prompts(
    prompt_id int auto_increment,
    team_id int,
    date_time datetime,
    prompt LONGTEXT,
    image LONGTEXT,
    submitted boolean,
    submission_id int,
    PRIMARY KEY(prompt_id),
    FOREIGN KEY (team_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (submission_id) REFERENCES submission(submission_id) ON DELETE CASCADE
);

CREATE TABLE assigned_submissions(
    submission_id int,
    img_grader_id int,
    prompt_grader_id int,
    img1_comment text,
    img2_comment text,
    prompt1_comment text,
    prompt2_comment text,
    img1_score float,
    img2_score float,
    prompt1_score float,
    prompt2_score float,
    status boolean,
    modified_date datetime,
    PRIMARY KEY(submission_id, img_grader_id, prompt_grader_id),
    FOREIGN KEY(submission_id) REFERENCES submission(submission_id) ON DELETE CASCADE,
	FOREIGN KEY(img_grader_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY(prompt_grader_id) REFERENCES user(user_id) ON DELETE CASCADE
);

INSERT INTO user(username, group_id, salt, hashed_pw)
VALUES("usr00001", 0, "$2b$12$iN1uw2I0egcVe5NWxLYlsu", "$2b$12$iN1uw2I0egcVe5NWxLYlsuv5fQH6NdwCZwpc4BA5xSMLXG/hsBN6q");

-- username: usr00001
-- password: yyCGR

INSERT INTO user(username, name, email, group_id)
VALUES
	("usr00001", "Thịnh Nguyễn", "sorrenw@gmail.com", 0),
    ("usr00002", "team_1", "aaa@gmail.com", 2),
    ("usr00003", "grader_1", "asw@gmail.com", 1),
	("usr00004", "team_2", "aaa@gmail.com", 2),
    ("usr00005", "grader_2", "aaa@gmail.com", 1),
    ("usr00006", "grader_3", "aaa@gmail.com", 1);
    
INSERT INTO submission(submit_date, assigned)
VALUES
	("2024-11-23", 1),
    ("2024-11-23", 1);

INSERT INTO prompts(team_id, prompt, image, submitted, submission_id)
VALUES
	(2, "abc", "b64", 1, 1),
    (2, "xyz", "b64", 1, 1),
    (2, "qwerty", "b64", 0, null),
    (4, "cba", "b64", 0, null),
    (4, "zyx", "b64", 1, 2),
    (4, "ytrewq", "b64", 1, 2);

-- INSERT INTO submission(prompt_id, assigned)
-- VALUES
-- 	(1, 1),
--     (5,1);

INSERT INTO assigned_submissions(submission_id, img_grader_id, prompt_grader_id, status)
VALUES
	(1, 3,  6, 0),
    (2, 3,5, 0);
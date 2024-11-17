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
    assigned boolean,
    PRIMARY KEY(submission_id),
    FOREIGN KEY(prompt_id) REFERENCES prompts(prompt_id)
);

CREATE TABLE assigned_submissions(
    submission_id int,
    img_grader_id int,
    video_grader_id int,
    prompt_grader_id int,
    img_comment text,
    video_comment text,
    prompt_comment text,
    img_score float,
    video_score float,
    prompt_score float,
    status boolean,
    modified_date datetime,
    PRIMARY KEY(submission_id, img_grader_id, video_grader_id, prompt_grader_id),
    FOREIGN KEY(submission_id) REFERENCES submission(submission_id),
	FOREIGN KEY(img_grader_id) REFERENCES user(user_id),
    FOREIGN KEY(video_grader_id) REFERENCES user(user_id),
    FOREIGN KEY(prompt_grader_id) REFERENCES user(user_id)
);

INSERT INTO user(username, name, email, group_id)
VALUES
	("usr00000", "Thịnh Nguyễn", "sorrenw@gmail.com", 0),
    ("usr00001", "abcxyz", "aaa@gmail.com", 2),
    ("usr00002", "asdfas", "asw@gmail.com", 1),
	("usr00003", "wqtah", "aaa@gmail.com", 2),
    ("usr00004", "qwetasd", "aaa@gmail.com", 1),
    ("usr00005", "skwoiyjkj", "aaa@gmail.com", 1);
    
INSERT INTO user(username, group_id, salt, hashed_pw)
VALUES("usr00006", 2, "$2b$12$BZyS/bsY816Aw5tZADVMLe", "$2b$12$BZyS/bsY816Aw5tZADVMLeSGEklXB2346NneyjXEPN/CcRXjcslou");
    
INSERT INTO prompts(team_id, prompt, image, submitted)
VALUES
	(2, "abc", "b64", 1),
    (2, "xyz", "b64", 0),
    (2, "qwerty", "b64", 0),
    (3, "abc", "b64", 0),
    (3, "xyz", "b64", 1),
    (3, "qwerty", "b64", 0);

INSERT INTO submission(prompt_id, video, assigned)
VALUES
	(1, "sample_url", 0),
    (5, "sample_url", 0);

-- INSERT INTO submission(prompt_id, video, assigned)
-- VALUES
-- 	(1, "sample_url", 1),
--     (5, "sample_url", 1);

INSERT INTO assigned_submissions(submission_id, img_grader_id, video_grader_id, prompt_grader_id, status)
VALUES
	(1, 3, 5, 6, 0),
    (2, 3, 3, 6, 0);

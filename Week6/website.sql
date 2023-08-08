SHOW DATABASES; 
CREATE DATABASE website; 


USE website; 
SHOW TABLES;

#刪除刪除刪除不要誤點
DROP DATABASE website; 

CREATE TABLE member (
    id BIGINT PRIMARY KEY AUTO_INCREMENT ,
    name VARCHAR(255) NOT NULL ,
    username VARCHAR(255) NOT NULL ,
    password VARCHAR(255) NOT NULL 
);
SELECT * FROM member;

CREATE TABLE message (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  member_id BIGINT NOT NULL,
  content VARCHAR(255) NOT NULL,
  time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (member_id) REFERENCES member(id)
);
INSERT INTO message (member_id, content)
VALUES (1, '這是第3筆留言');
SELECT * FROM message;

SELECT message.content, member.name FROM message JOIN member ON member.id = message.member_id WHERE member.username = '111';
SELECT * FROM member WHERE username ='111';
SELECT * FROM message ORDER BY time DESC;






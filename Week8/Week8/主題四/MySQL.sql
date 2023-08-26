CREATE DATABASE websiteW5; 
SHOW DATABASES; 

USE websiteW5; 
SHOW TABLES;

drop database websiteW5; #刪除刪除刪除不要誤點

CREATE TABLE member (
    id BIGINT PRIMARY KEY AUTO_INCREMENT ,
    name VARCHAR(255) NOT NULL ,
    username VARCHAR(255) NOT NULL ,
    password VARCHAR(255) NOT NULL ,
    follower_count INT UNSIGNED NOT NULL DEFAULT 0 , 
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP 
);

INSERT INTO member (name, username, password,follower_count)
VALUES ('test', 'test', 'test',10);
INSERT INTO member (name, username, password,follower_count)
VALUES 
('name1', 'username1', 'password1',100);
INSERT INTO member (name, username, password,follower_count)
VALUES 
('name2', 'username2', 'password2',200);
INSERT INTO member (name, username, password,follower_count)
VALUES 
('name3', 'username3', 'password3',300);
INSERT INTO member (name, username, password,follower_count)
VALUES 
('name4', 'username4', 'password4',400);

CREATE TABLE message (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  member_id BIGINT NOT NULL,
  content VARCHAR(255) NOT NULL,
  like_count INT UNSIGNED NOT NULL DEFAULT 0,
  time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (member_id) REFERENCES member(id)
);

INSERT INTO message (member_id, content, like_count)
VALUES (1, '這是test留言1', 5);
INSERT INTO message (member_id, content, like_count)
VALUES (1, '這是test留言2', 10);
INSERT INTO message (member_id, content, like_count)
VALUES (1, '這是test留言3', 15);
INSERT INTO message (member_id, content, like_count)
VALUES (2, '這是第一筆留言', 20);
INSERT INTO message (member_id, content, like_count)
VALUES (3, '這是第二筆留言', 25);
INSERT INTO message (member_id, content, like_count)
VALUES (4, '這是第三筆留言', 30);
INSERT INTO message (member_id, content, like_count)
VALUES (5, '這是第四筆留言', 35);

/*---------主鍵完整性-----------*/
DELETE FROM member WHERE id = '5';

INSERT INTO message (member_id, content, like_count)
VALUES (999, '這是第四999筆留言', 35);

/*----------------------提高搜索速度-----------------------*/
SELECT * FROM member;

/*總共檢查5筆資料*/
EXPLAIN 
SELECT * FROM member WHERE username = 'test';

/*建立index*/
ALTER TABLE member ADD INDEX username_index(username);
/*再次搜尋，可以發現只檢查1筆*/

ALTER TABLE member ADD INDEX password_index(password);
ALTER TABLE member DROP INDEX username_index;

EXPLAIN
SELECT * FROM member WHERE username = 'test' AND password = 'test';
/*雖然用username檢查出1筆資料，但是password還是要檢查這一筆是否有符合test的資料，所以還是要進行全部的比對*/

/*複合索引*/
ALTER TABLE member ADD INDEX index_username_password (username, password);
ALTER TABLE member DROP INDEX index_username_password;


/*----------------------部分關鍵字-----------------*/
SELECT * FROM message;

EXPLAIN
SELECT * FROM message WHERE content LIKE '%test%';
/*因為是部分關鍵字搜尋，所以設定索引沒有甚麼效果*/










CREATE DATABASE website; 
SHOW DATABASES; 

USE website; 
SHOW TABLES;

SELECT * FROM member;
SHOW CREATE TABLE member; #可以看整個資料表結構，包含附註
drop database website; #刪除刪除刪除不要誤點

/*---------------任務二-----------------------*/
CREATE TABLE member (
    id BIGINT PRIMARY KEY AUTO_INCREMENT , #BIGINT 是一種大整數型別，可以儲存更大範圍的整數值。
    name VARCHAR(255) NOT NULL ,
    username VARCHAR(255) NOT NULL ,
    password VARCHAR(255) NOT NULL ,
    follower_count INT UNSIGNED NOT NULL DEFAULT 0 , #INT UNSIGNED 是無符號整數型別，只能儲存非負整數值。
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP #CURRENT_TIMESTAMP插入資料時，可以獲取當下的時間
);

/*----------------------任務三-----------------------*/
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

SELECT * FROM member;

SELECT * FROM member ORDER BY time DESC; #ASC小到大；DESC大到小

SELECT * FROM member ORDER BY time DESC LIMIT 3 OFFSET 1; #LIMIT取得三筆資料；OFFSET跳過前面一筆 

SELECT * FROM member WHERE username = 'test';

SELECT * FROM member WHERE username = 'test' AND password = 'test';

/*先關閉MySQL Workbench的安全設定*/
SET SQL_SAFE_UPDATES=0;
UPDATE member SET name = 'test2' WHERE username = 'test';

/*----------------------任務四-----------------------*/
SELECT COUNT(id) FROM member;
SELECT SUM(follower_count) FROM member;
SELECT AVG(follower_count) FROM member;
/*----------------------任務五-----------------------*/
SELECT * FROM message;

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

SELECT message.content,member.name
FROM message
JOIN member ON member.id = message.member_id;

SELECT message.content, member.name
FROM message
JOIN member ON member.id = message.member_id
WHERE member.username = 'test';

SELECT AVG(message.like_count)
FROM message
JOIN member ON member.id = message.member_id
WHERE member.username = 'test';
/*----------------------提高搜索速度-----------------------*/
/*explain 可以了解細節運作*/ 
/*檢查五筆資料，整個資料的百分之20%是我們要的資料*/
EXPLAIN 
SELECT * FROM member WHERE username = 'test';

/*index 建立樹狀結構，可以提高搜尋速度*/
/*新增索引 alter table 資料表 add index 索引名稱(參考的欄位名稱)*/
ALTER TABLE member ADD INDEX username_index(username);
ALTER TABLE member ADD INDEX password_index(password);
ALTER TABLE member DROP INDEX password_index;


EXPLAIN
SELECT * FROM member WHERE username = 'test' AND password = 'test';
/*複合索引*/
ALTER TABLE member ADD INDEX index_username_password (username, password);
ALTER TABLE member DROP INDEX index_username_password



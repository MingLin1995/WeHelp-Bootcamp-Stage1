SHOW DATABASES; 
CREATE DATABASE website; 

USE website; 
SHOW TABLES;

#刪除刪除刪除不要誤點
DROP DATABASE websiteW5; 

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
SELECT * FROM message;


CREATE TABLE token (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    member_id BIGINT NOT NULL,
    token VARCHAR(500) NOT NULL,
    FOREIGN KEY (member_id) REFERENCES member(id)
);

SELECT * FROM token;

INSERT INTO member (name, username, password) VALUES ('test','test', 'test');
ANALYZE TABLE member;


/*------------------------------------------------*/
SELECT * FROM member;
/*單一條件*/
EXPLAIN 
SELECT * FROM member WHERE username = 'test';
/*查詢37筆資料*/

/*建立索引*/
ALTER TABLE member ADD INDEX username_index(username);
ALTER TABLE member DROP INDEX username_index;

/*多個條件*/
EXPLAIN 
SELECT * FROM member WHERE username='test' and password='test';

ALTER TABLE member ADD INDEX index_username_password (username, password);
ALTER TABLE member DROP INDEX index_username_password;

/*關鍵字搜尋*/
SELECT * FROM message;

EXPLAIN
SELECT * FROM message WHERE content LIKE '%密碼%';
/*共有六筆*/

/*因為是部分關鍵字搜尋，所以設定索引沒有甚麼效果*/
ALTER TABLE message ADD INDEX content_index(content);
ALTER TABLE message DROP INDEX content_index;













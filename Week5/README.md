### 任務三
* 使⽤ INSERT 指令新增⼀筆資料到 member 資料表中，這筆資料的 username 和password 欄位必須是 test。接著繼續新增⾄少 4 筆隨意的資料。
```MySQL=
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
```
<img width="538" alt="image" src="https://github.com/MingLin1995/WeHelp-Bootcamp-Stage1/assets/125284928/ac7941e1-0a0c-4aa3-ae85-e3f777f05127">
---
* 使⽤ SELECT 指令取得所有在 member 資料表中的會員資料。
```MySQL=
SELECT * FROM member;
```
![image](https://github.com/MingLin1995/WeHelp-Bootcamp-Stage1/assets/125284928/529ce1c8-a8d1-4dc9-9731-7cc399d25208)
---

* 使⽤ SELECT 指令取得所有在 member 資料表中的會員資料，並按照 time 欄位，由近到遠排序。
```MySQL=
SELECT * FROM member ORDER BY time DESC;
```
![image](https://github.com/MingLin1995/WeHelp-Bootcamp-Stage1/assets/125284928/535beb1f-2ef8-4b67-921d-02c9fedd64ad)
---

* 使⽤ SELECT 指令取得 member 資料表中第 2 到第 4 筆共三筆資料，並按照 time 欄位，由近到遠排序。 ( 並非編號 2、3、4 的資料，⽽是排序後的第 2 ~ 4 筆資料 )
```MySQL=
SELECT * FROM member ORDER BY time DESC LIMIT 3 OFFSET 1;
```
![image](https://github.com/MingLin1995/WeHelp-Bootcamp-Stage1/assets/125284928/5a992937-7cff-41ad-b227-b45957cb1fea)
---

* 使⽤ SELECT 指令取得欄位 username 是 test 的會員資料。
```MySQL=
SELECT * FROM member WHERE username = 'test';
```
![image](https://github.com/MingLin1995/WeHelp-Bootcamp-Stage1/assets/125284928/cb0172bb-9e46-4c7b-a30a-4a257713582e)
---

* 使⽤ SELECT 指令取得欄位 username 是 test、且欄位 password 也是 test 的資料。
```MySQL=
SELECT * FROM member WHERE username = 'test' AND password = 'test';
```
![image](https://github.com/MingLin1995/WeHelp-Bootcamp-Stage1/assets/125284928/4cdd3c1a-f349-4fa3-8608-db67ce9cccaa)
---

* 使⽤ UPDATE 指令更新欄位 username 是 test 的會員資料，將資料中的 name 欄位改成 test2。
```MySQL=
SET SQL_SAFE_UPDATES=0;
UPDATE member SET name = 'test2' WHERE username = 'test';
```
<img width="291" alt="image" src="https://github.com/MingLin1995/WeHelp-Bootcamp-Stage1/assets/125284928/7a32f4da-30e3-4264-9ac4-a9ca2380068e">
---

### 任務四
* 取得 member 資料表中，總共有幾筆資料 ( 幾位會員 )。
```MySQL=
SELECT COUNT(id) FROM member;
```
![image](https://github.com/MingLin1995/WeHelp-Bootcamp-Stage1/assets/125284928/490a70e1-5542-44de-af0f-6d24fa3a6a9f)
---

* 取得 member 資料表中，所有會員 follower_count 欄位的總和。
```MySQL=
SELECT SUM(follower_count) FROM member;
```
![image](https://github.com/MingLin1995/WeHelp-Bootcamp-Stage1/assets/125284928/e5e25536-3902-4b35-a209-207001c6b1e2)


* 取得 member 資料表中，所有會員 follower_count 欄位的平均數。
```MySQL=
SELECT AVG(follower_count) FROM member;
```
![image](https://github.com/MingLin1995/WeHelp-Bootcamp-Stage1/assets/125284928/fbd05b91-fd49-47e4-9526-eef8c9b26535)
---


### 任務五
![image](https://github.com/MingLin1995/WeHelp-Bootcamp-Stage1/assets/125284928/db0b3e95-e56e-4bb7-b871-0e839380f025)
```MySQL=
CREATE TABLE message (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  member_id BIGINT NOT NULL,
  content VARCHAR(255) NOT NULL,
  like_count INT UNSIGNED NOT NULL DEFAULT 0,
  time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (member_id) REFERENCES member(id)
);
```
<img width="259" alt="image" src="https://github.com/MingLin1995/WeHelp-Bootcamp-Stage1/assets/125284928/9327762c-db64-47df-ab98-6221ccaa07ff">
---

* 使⽤ SELECT 搭配 JOIN 語法，取得所有留⾔，結果須包含留⾔者的姓名。
```MySQL=
SELECT message.content,member.name
FROM message
JOIN member ON member.id = message.member_id;
```
![image](https://github.com/MingLin1995/WeHelp-Bootcamp-Stage1/assets/125284928/42131839-c54d-41c2-8e54-c98cb036ba12)
---

* 使⽤ SELECT 搭配 JOIN 語法，取得 member 資料表中欄位 username 是 test 的所有留⾔，資料中須包含留⾔者的姓名。
```MySQL=
SELECT message.content, member.name
FROM message
JOIN member ON member.id = message.member_id
WHERE member.username = 'test';
```
![image](https://github.com/MingLin1995/WeHelp-Bootcamp-Stage1/assets/125284928/53c4efe6-740c-48b2-af97-7d974f420b1c)
---

* 使⽤ SELECT、SQL Aggregate Functions 搭配 JOIN 語法，取得 member 資料表中欄位 username 是 test 的所有留⾔平均按讚數。
```MySQL=
SELECT AVG(message.like_count)
FROM message
JOIN member ON member.id = message.member_id
WHERE member.username = 'test';
```
![image](https://github.com/MingLin1995/WeHelp-Bootcamp-Stage1/assets/125284928/7a105ef9-7e62-444a-9540-ea0125d59250)
---


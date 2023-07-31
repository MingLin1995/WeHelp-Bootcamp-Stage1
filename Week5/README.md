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

* 使⽤ SELECT 指令取得所有在 member 資料表中的會員資料。
```MySQL=
SELECT * FROM member;
```
![](https://hackmd.io/_uploads/ryrvg7Ss2.png)

* 使⽤ SELECT 指令取得所有在 member 資料表中的會員資料，並按照 time 欄位，由近到遠排序。
```MySQL=
SELECT * FROM member ORDER BY time DESC;
```
![](https://hackmd.io/_uploads/HyCTeXHo3.png)

* 使⽤ SELECT 指令取得 member 資料表中第 2 到第 4 筆共三筆資料，並按照 time 欄位，由近到遠排序。 ( 並非編號 2、3、4 的資料，⽽是排序後的第 2 ~ 4 筆資料 )
```MySQL=
SELECT * FROM member ORDER BY time DESC LIMIT 3 OFFSET 1;
```
![](https://hackmd.io/_uploads/HkDQZmHin.png)

* 使⽤ SELECT 指令取得欄位 username 是 test 的會員資料。
```MySQL=
SELECT * FROM member WHERE username = 'test';
```
![](https://hackmd.io/_uploads/SyR9Zmrj2.png)

* 使⽤ SELECT 指令取得欄位 username 是 test、且欄位 password 也是 test 的資料。
```MySQL=
SELECT * FROM member WHERE username = 'test' AND password = 'test';
```
![](https://hackmd.io/_uploads/SyEPM7Sih.png)

* 使⽤ UPDATE 指令更新欄位 username 是 test 的會員資料，將資料中的 name 欄位改成 test2。
```MySQL=
SET SQL_SAFE_UPDATES=0;
UPDATE member SET name = 'test2' WHERE username = 'test';
```

### 任務四
* 取得 member 資料表中，總共有幾筆資料 ( 幾位會員 )。
```MySQL=
SELECT COUNT(id) FROM member;
```
![](https://hackmd.io/_uploads/HyPeEQHih.png)

* 取得 member 資料表中，所有會員 follower_count 欄位的總和。
```MySQL=
SELECT SUM(follower_count) FROM member;
```
![](https://hackmd.io/_uploads/SkEMVXHih.png)

* 取得 member 資料表中，所有會員 follower_count 欄位的平均數。
```MySQL=
SELECT AVG(follower_count) FROM member;
```
![](https://hackmd.io/_uploads/BkLvN7ri3.png)


### 任務五
![](https://hackmd.io/_uploads/B18qIQHi2.png)
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
* 使⽤ SELECT 搭配 JOIN 語法，取得所有留⾔，結果須包含留⾔者的姓名。
```MySQL=
SELECT message.content,member.name
FROM message
JOIN member ON member.id = message.member_id;
```
![](https://hackmd.io/_uploads/rJYyu7Bsh.png)

* 使⽤ SELECT 搭配 JOIN 語法，取得 member 資料表中欄位 username 是 test 的所有留⾔，資料中須包含留⾔者的姓名。
```MySQL=
SELECT message.content, member.name
FROM message
JOIN member ON member.id = message.member_id
WHERE member.username = 'test';
```
![](https://hackmd.io/_uploads/SkSz_mBo2.png)

* 使⽤ SELECT、SQL Aggregate Functions 搭配 JOIN 語法，取得 member 資料表中欄位 username 是 test 的所有留⾔平均按讚數。
```MySQL=
SELECT AVG(message.like_count)
FROM message
JOIN member ON member.id = message.member_id
WHERE member.username = 'test';
```
![](https://hackmd.io/_uploads/B1nXOQSih.png)

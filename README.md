# 驾校一点通驾考理论题爬虫

通过爬取驾校一点通的get_question接口获取驾考理论题库，并通过pymysql将题目信息直接存储在mysql数据库中，图库存储在指定目录。

## 部署方法

基础环境：`python3`, `pip3`

1. `pip3 install pymysql`

   `pip3 install requests`

2. 使用mysql创建questions数据表，建表sql代码如下：

   ```mysql
   CREATE TABLE `questions` (
     `id` int(11) NOT NULL,
     `question` varchar(255) NOT NULL,
     `a` varchar(255) DEFAULT NULL,
     `b` varchar(255) DEFAULT NULL,
     `c` varchar(255) DEFAULT NULL,
     `d` varchar(255) DEFAULT NULL,
     `ta` varchar(255) DEFAULT NULL,
     `imageurl` varchar(255) DEFAULT NULL,
     `bestanswer` varchar(255) DEFAULT NULL,
     `bestanswerid` varchar(255) DEFAULT NULL,
     `type` int(11) DEFAULT NULL,
     `sinaimg` varchar(255) DEFAULT NULL,
     `options` varchar(255) DEFAULT NULL
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
   ALTER TABLE `questions`
     ADD PRIMARY KEY (`id`);
   ALTER TABLE `questions`
     MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
   COMMIT;
   ```

   

3. 打开`main.py`文件，配置第九行的数据库连接信息，配置第40行图片文件的储存位置，配置第42行图片的链接，如果没有网址的话，这行要删掉

4. `python3 main.py`
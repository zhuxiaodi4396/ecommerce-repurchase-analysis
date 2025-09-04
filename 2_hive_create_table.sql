-- 创建数据库
CREATE DATABASE IF NOT EXISTS ecommerce_db;
USE ecommerce_db;

-- 创建外部表（直接关联 HDFS 目录，无需额外加载）
CREATE EXTERNAL TABLE IF NOT EXISTS user_behavior (
    user_id STRING,
    item_id STRING,
    category_id STRING,
    behavior_type STRING,  -- 'pv'浏览/'fav'收藏/'cart'加购/'buy'购买
    ts BIGINT,  -- 时间戳字段
    datetime STRING,
    month INT,
    weekday INT,
    hour INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION '/user/ecommerce/cleaned_data';  -- 直接关联 HDFS 目录
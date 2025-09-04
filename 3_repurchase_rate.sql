USE ecommerce_db;

-- 1. 提取 11 月购买用户
CREATE TABLE IF NOT EXISTS nov_buy_users AS
SELECT DISTINCT user_id
FROM user_behavior
WHERE month = 11 AND behavior_type = 'buy';

-- 2. 提取 12 月购买用户
CREATE TABLE IF NOT EXISTS dec_buy_users AS
SELECT DISTINCT user_id
FROM user_behavior
WHERE month = 12 AND behavior_type = 'buy';

-- 3. 计算复购用户（11 月买且 12 月买）
CREATE TABLE IF NOT EXISTS repurchase_users AS
SELECT a.user_id
FROM nov_buy_users a
JOIN dec_buy_users b ON a.user_id = b.user_id;

-- 4. 计算整体复购率 = 复购用户数 / 11 月购买用户数
SELECT
  (COUNT(DISTINCT r.user_id) / COUNT(DISTINCT n.user_id)) * 100 AS repurchase_rate_pct
FROM nov_buy_users n
LEFT JOIN repurchase_users r ON n.user_id = r.user_id;

-- 5. 分品类复购率（11 月买过该品类且 12 月再次购买该品类）
SELECT
  t1.category_id,
  (COUNT(DISTINCT t2.user_id) / COUNT(DISTINCT t1.user_id)) * 100 AS category_repurchase_pct
FROM (
  SELECT DISTINCT user_id, category_id
  FROM user_behavior
  WHERE month = 11 AND behavior_type = 'buy'
) t1
LEFT JOIN (
  SELECT DISTINCT user_id, category_id
  FROM user_behavior
  WHERE month = 12 AND behavior_type = 'buy'
) t2 ON t1.user_id = t2.user_id AND t1.category_id = t2.category_id
GROUP BY t1.category_id
ORDER BY category_repurchase_pct DESC;
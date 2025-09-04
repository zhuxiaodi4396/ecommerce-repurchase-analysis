# 电商用户复购率分析项目

## 项目背景
淘宝"双11"后用户复购率下滑问题（实际复购率15% vs 行业均值25%），通过数据分析定位原因并提出优化策略，助力提升用户留存与平台营收。

## 数据来源
使用天池公开数据集《User Behavior Data from Taobao for Recommendation》，包含100万条用户行为记录，字段包括用户ID、商品ID、品类ID、行为类型（浏览/收藏/加购/购买）、时间戳等。

## 技术栈
- 数据处理：Python（Pandas）
- 数据分析：SQL（Hive）
- 可视化：Matplotlib、Seaborn
- 大数据存储：Hadoop HDFS

## 项目结构
1. `1_data_preprocessing.py`：数据清洗与预处理代码
2. `2_hive_create_table.sql`：Hive表创建脚本
3. `3_repurchase_rate.sql`：复购率计算SQL
4. `4_behavior_analysis.py`：用户行为分析与可视化
5. `analysis_report.md`：分析结论与策略建议

## 核心结论
- 整体复购率15%，3C品类复购率仅8%（主要拖累因素）
- 复购用户"浏览→加购→购买"转化率（35%）显著高于非复购用户（8%）
- 商品评价≥4.5分、无售后投诉的用户复购率更高

## 优化建议
1. 优化3C品类售后流程，降低投诉率
2. 针对非复购用户，在周末20:00-22:00推送加购商品优惠券
3. 首页突出展示高复购率、高评价商品

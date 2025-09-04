import pandas as pd
import numpy as np

# 1. 读取数据（100万条，采样10万条加速处理）
df = pd.read_csv('user_behavior.csv', header=None,
                 names=['user_id', 'item_id', 'category_id', 'behavior_type', 'timestamp'])
df_sample = df.sample(n=100000, random_state=42)  # 随机采样

# 2. 缺失值处理
missing = df_sample.isnull().sum()
print(f"缺失值统计：\n{missing}")  # 实际数据集通常无缺失，模拟处理逻辑
df_clean = df_sample.dropna(subset=['behavior_type'])  # 删除行为类型缺失的记录

# 3. 异常值处理
# 3.1 时间范围过滤（聚焦2017-11-01至2017-12-31，原数据集时间）
df_clean['datetime'] = pd.to_datetime(df_clean['timestamp'], unit='s')
start_date = pd.to_datetime('2017-11-01')
end_date = pd.to_datetime('2017-12-31')
df_clean = df_clean[(df_clean['datetime'] >= start_date) & (df_clean['datetime'] <= end_date)]

# 3.2 过滤异常用户（单日行为>100次可能为刷单）
daily_behavior = df_clean.groupby(['user_id', df_clean['datetime'].dt.date]).size()
abnormal_users = daily_behavior[daily_behavior > 100].index.get_level_values('user_id').unique()
df_clean = df_clean[~df_clean['user_id'].isin(abnormal_users)]

# 4. 特征衍生
df_clean['month'] = df_clean['datetime'].dt.month  # 11月/12月
df_clean['weekday'] = df_clean['datetime'].dt.weekday  # 周几（0=周一）
df_clean['hour'] = df_clean['datetime'].dt.hour  # 小时

# 5. 保存清洗后的数据
df_clean.to_csv('cleaned_user_behavior.csv', index=False)
print(f"清洗完成，剩余数据量：{len(df_clean)}条")

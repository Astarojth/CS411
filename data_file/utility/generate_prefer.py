import pandas as pd
import numpy as np
import random

# 读取CSV文件
users = pd.read_csv("users.csv")
games = pd.read_csv("game_info.csv")

# 基于玩家数量对QueryID进行加权选择
weights = games['Players'].fillna(0).values
weights = weights / weights.sum()
selected_queries = np.random.choice(games['QueryID'], size=12460, p=weights)

# 随机选择UserID
selected_users = np.random.choice(users['UserID'], size=12460)

# 创建新的DataFrame
df = pd.DataFrame({
    'UserID': selected_users,
    'QueryID': selected_queries
})

# 将CategoryID和GenreID添加到新的DataFrame
df = df.merge(games[['QueryID', 'CategoryID', 'GenreID']], on='QueryID', how='left')

# 保存结果到Excel文件
df.to_excel("game_preference.xlsx", index=False)

print("game_preference.xlsx has been saved!")

import pandas as pd

# 读取Excel文件
file_path = 'games-database.xlsx'
xls = pd.read_excel(file_path, engine='openpyxl', sheet_name=None)

# 若文件中存在'main'工作表，则进行处理
if 'main' in xls:
    df = xls['main']
    
    # 计算PlatformID的值
    def calculate_platform_id(row):
        platform_id = 0
        if row.get('PlatformWindows', False):
            platform_id += 4
        if row.get('PlatformLinux', False):
            platform_id += 2
        if row.get('PlatformMac', False):
            platform_id += 1
        return platform_id

    df['PlatformID'] = df.apply(calculate_platform_id, axis=1)
    
    # 删除指定的列
    df.drop(columns=['PlatformWindows', 'PlatformLinux', 'PlatformMac'], inplace=True)
    
    # 保存修改后的工作表回xls字典
    xls['main'] = df

# 保存修改后的数据回Excel文件
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    for sheet_name, data in xls.items():
        data.to_excel(writer, sheet_name=sheet_name, index=False)

print("PlatformID has been updated and columns have been removed.")

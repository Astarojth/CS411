import pandas as pd
file_path = 'games-database.xlsx'
df = pd.read_excel(file_path, engine='openpyxl',sheet_name='main')
def is_float_or_zero(val):
    try:
        return float(val) == val or val == 0
    except:
        return False
df = df[df['PriceFinal'].apply(is_float_or_zero)]
df.to_excel(file_path, index=False, engine='openpyxl')
#part2
df = pd.read_excel(file_path, sheet_name='main', engine='openpyxl')
df = df[df['Players'] != 0]
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
    workbook = writer.book
    if 'main' in workbook.sheetnames:
        del workbook['main']
    df.to_excel(writer, sheet_name='main', index=False)

print(f"Rows where Players is 0 have been deleted in {file_path}")
import pandas as pd
num_categories = 256 
columns = ["CategoryID", "CategorySinglePlayer", "CategoryMultiplayer", "CategoryCoop", "CategoryMMO", "CategoryInAppPurchase", "CategoryIncludeSrcSDK", "CategoryIncludeLevelEditor", "CategoryVRSupport"]
df = pd.DataFrame(columns=columns)

for i in range(num_categories):
    binary_representation = format(i, '08b')
    row = {"CategoryID": i}
    for idx, col in enumerate(columns[1:], 1):  
        row[col] = binary_representation[-idx] == '1'  
        
    df.loc[i] = row 


output_file = "categories.xlsx"
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"Data has been saved to {output_file}")

file_path = "games-database.xlsx" 
df = pd.read_excel(file_path, engine='openpyxl', sheet_name='main')

category_columns = [
    "CategorySinglePlayer", "CategoryMultiplayer", "CategoryCoop", 
    "CategoryMMO", "CategoryInAppPurchase", "CategoryIncludeSrcSDK", 
    "CategoryIncludeLevelEditor", "CategoryVRSupport"
]

def compute_category_id(row):
    binary_representation = ''.join(['1' if row[col] else '0' for col in category_columns])
    return int(binary_representation, 2)

df['CategoryID'] = df.apply(compute_category_id, axis=1)

df = df.drop(columns=category_columns)

with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
    workbook = writer.book
    if 'main' in workbook.sheetnames:
        del workbook['main']
    df.to_excel(writer, sheet_name='main', index=False)

print(f"Columns have been updated and CategoryID has been added in {file_path}")


import pandas as pd

num_categories = 2**13 
columns = ['GenreID','GenreIsNonGame','GenreIsIndie','GenreIsAction','GenreIsAdventure','GenreIsCasual','GenreIsStrategy','GenreIsRPG','GenreIsSimulation','GenreIsEarlyAccess','GenreIsFreeToPlay','GenreIsSports','GenreIsRacing','GenreIsMassivelyMultiplayer']
df = pd.DataFrame(columns=columns)

for i in range(num_categories):
    binary_representation = format(i, '13b')
    row = {"GenreID": i}
    for idx, col in enumerate(columns[1:], 1): 
        row[col] = binary_representation[-idx] == '1'
        
    df.loc[i] = row 
output_file = "genre.xlsx"
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"Data has been saved to {output_file}")

file_path = "games-database.xlsx"
df = pd.read_excel(file_path, engine='openpyxl', sheet_name='main')

genre_columns = [
    'GenreIsNonGame','GenreIsIndie','GenreIsAction','GenreIsAdventure','GenreIsCasual','GenreIsStrategy','GenreIsRPG','GenreIsSimulation','GenreIsEarlyAccess','GenreIsFreeToPlay','GenreIsSports','GenreIsRacing','GenreIsMassivelyMultiplayer'
]

def compute_genre_id(row):
    binary_representation = ''.join(['1' if row[col] else '0' for col in genre_columns])
    return int(binary_representation, 2)

df['GenreID'] = df.apply(compute_genre_id, axis=1)

df = df.drop(columns=genre_columns)

with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
    workbook = writer.book
    if 'main' in workbook.sheetnames:
        del workbook['main']
    df.to_excel(writer, sheet_name='main', index=False)

print(f"Columns have been updated and genreID has been added in {file_path}")


# Combines the multiple CSV files into one, based on system index
import csv

files_to_combine = [
    'data/BurnedArea-100k.csv',
    'data/Elevation-100k.csv',
    'data/Forest-100k.csv',
    'data/HumanModification-100k.csv',
    'data/LeafArea-100k.csv',
    'data/Precipitation-100k.csv',
    'data/SoilType-100k.csv',
    'data/Temperature-100k.csv',
    'data/Radiation-100k.csv'
]

entire_dict = {}
all_keys = []

for file_to_combine in files_to_combine:
    with open(file_to_combine) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        print('Reading', file_to_combine)
        for row in csv_reader:
            system_index = row['system:index']
            if system_index not in entire_dict:
                entire_dict[system_index] = {}
            row_dict = entire_dict[system_index]
            for key, value in row.items():
                if key not in all_keys:
                    all_keys.append(key)
                if key is not 'system:index':
                    row_dict[key] = value
# Convert the dict to a list of dicts
dict_list = []
for system_index, inner_dict in entire_dict.items():
    inner_dict_copy = inner_dict.copy()
    inner_dict_copy['system:index'] = system_index
    dict_list.append(inner_dict_copy)
dict_list.sort(key=lambda x: int(x['system:index'].split('_')[0]))

# Write the output to a CSV
output_file_name = 'data/all_training_data.csv'
with open(output_file_name, 'w') as output_file:
    w = csv.DictWriter(output_file, all_keys)
    w.writeheader()
    for dict_row in dict_list:
        w.writerow(dict_row)
print('Wrote output to file', output_file_name)
import pandas as pd

pd.set_option('display.max_columns', 8)

files_to_read = ["general.csv", "prenatal.csv", "sports.csv"]
for file in files_to_read:
    csv_data = pd.read_csv("test/" + file)
    print(csv_data.head(20))

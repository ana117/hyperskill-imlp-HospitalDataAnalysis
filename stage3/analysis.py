import pandas as pd

pd.set_option('display.max_columns', 8)

csv_data = {}
files_to_read = ["general", "prenatal", "sports"]
for file_name in files_to_read:
    csv_data[file_name] = pd.read_csv(f"test/{file_name}.csv")

    # rename columns excepts general.csv
    if file_name != "general":
        csv_data[file_name].columns = csv_data["general"].columns

combined_data = pd.concat(csv_data.values(), ignore_index=True)
combined_data.drop(columns="Unnamed: 0", inplace=True)

# drop empty row
combined_data.dropna(how="all", inplace=True)

# change gender to f/m
combined_data["gender"].replace(["female", "woman"], "f", inplace=True)
combined_data["gender"].replace(["male", "man"], "m", inplace=True)

# replace prenatal NaN with f
combined_data["gender"].fillna("f", inplace=True)

# replace Nan with zero
columns_to_change = ["bmi", "diagnosis", "blood_test", "ecg", "ultrasound", "mri", "xray", "children", "months"]
for column in columns_to_change:
    combined_data[column].fillna(0, inplace=True)

print(combined_data.shape)
print(combined_data.sample(n=20, random_state=30))

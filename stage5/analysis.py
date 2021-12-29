import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 8)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)


def getHospitalX(data_frame, hospital_name):
    return data_frame.loc[df["hospital"] == hospital_name]


csv_data = {}
files_to_read = ["general", "prenatal", "sports"]
for file_name in files_to_read:
    csv_data[file_name] = pd.read_csv(f"test/{file_name}.csv")

    # rename columns excepts general.csv
    if file_name != "general":
        csv_data[file_name].columns = csv_data["general"].columns

df = pd.concat(csv_data.values(), ignore_index=True)
df.drop(columns="Unnamed: 0", inplace=True)

# drop empty row
df.dropna(how="all", inplace=True)

# change gender to f/m
df["gender"].replace(["female", "woman"], "f", inplace=True)
df["gender"].replace(["male", "man"], "m", inplace=True)

# replace prenatal NaN with f
df["gender"].fillna("f", inplace=True)

# replace Nan with zero
columns_to_change = ["bmi", "diagnosis", "blood_test", "ecg", "ultrasound", "mri", "xray", "children", "months"]
for column in columns_to_change:
    df[column].fillna(0, inplace=True)

answers = []
# Q1: What is the most common age of a patient among all hospitals?
# Plot a histogram and choose one of the following age ranges: 0-15, 15-35, 35-55, 55-70, or 70-80
plt.figure(1)
counts, bins, bars = plt.hist(df["age"], bins=[0, 15, 35, 55, 70, 80])
plt.xticks([0, 15, 35, 55, 70, 80])

max_count_index = counts.tolist().index(max(counts))
most_common_age = f"{bins[max_count_index]}-{bins[max_count_index+1]}"
answers.append(most_common_age)


# Q2: What is the most common diagnosis among patients in all hospitals?
# Create a pie chart
plt.figure(2)
diagnosis_series = df["diagnosis"].value_counts()
plt.pie(diagnosis_series, labels=diagnosis_series.index)

most_common_diagnosis = diagnosis_series.idxmax()
answers.append(most_common_diagnosis)


# Q3: Build a violin plot of height distribution by hospitals.
# What is the main reason for the gap in values?
# Why there are two peaks, which correspond to the relatively small and big values?
plt.figure(3)
general_heights = df[df.hospital == "general"]["height"]
prenatal_heights = df[df.hospital == "prenatal"]["height"]
sports_heights = df[df.hospital == "sports"]["height"]
plt.violinplot(dataset=[general_heights, prenatal_heights, sports_heights],
               showmeans=True, showmedians=True,
               showextrema=True)
answers.append("General: All kinds of people | Prenatal: Woman | Sports: Athletes (not sure why reaching 5++)")

plt.show()

NUM_ORDER = ["1st", "2nd", "3rd"]
for i, answer in enumerate(answers):
    print(f"The answer to the {NUM_ORDER[i]} question: {answer}")

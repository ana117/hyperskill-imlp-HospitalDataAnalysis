import pandas as pd

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
# Q1: Which hospital has the highest number of patients?
grouped = df.groupby(["hospital"])["gender"].count()
max_count_hospital = grouped.idxmax()
answers.append(max_count_hospital)

# Q2: What share of the patients in the general hospital suffers from stomach-related issues?
#     Round the result to the third decimal place.
general_hospital = getHospitalX(df, "general")
total_cases_count = general_hospital.shape[0]
stomach_cases_count = general_hospital.loc[df["diagnosis"] == "stomach"].shape[0]
percentage = round(stomach_cases_count/total_cases_count, 3)
answers.append(percentage)

# Q3: What share of the patients in the sports hospital suffers from dislocation-related issues?
#     Round the result to the third decimal place.
sports_hospital = getHospitalX(df, "sports")
total_cases_count = sports_hospital.shape[0]
dislocation_cases_count = sports_hospital.loc[df["diagnosis"] == "dislocation"].shape[0]
percentage = round(dislocation_cases_count/total_cases_count, 3)
answers.append(percentage)

# Q4: What is the difference in the median ages of the patients in the general and sports hospitals?
general_hospital = getHospitalX(df, "general")
sports_hospital = getHospitalX(df, "sports")
general_median = general_hospital["age"].median()
sports_median = sports_hospital["age"].median()
difference = abs(general_median - sports_median)
answers.append(difference)

# Q5: In which hospital the blood test was taken the most often (there is the biggest number
# of t in the blood_test column among all the hospitals)?
# How many blood tests were taken?
grouped = df.groupby(["blood_test", "hospital"])["gender"].count()
pivoted = df.pivot_table(index="blood_test", columns="hospital", values="gender", aggfunc="count", fill_value=-1)
t_only = pivoted.loc["t"]
max_count = t_only.max()
max_count_hospital = t_only.idxmax()
answers.append((max_count_hospital, max_count))


NUM_ORDER = ["st", "nd", "rd", "th", "th"]
for i in range(len(answers)):
    q_number = f"{i+1}{NUM_ORDER[i]}"
    answer = answers[i]
    if i+1 == 5:
        answer = f"{answer[0]}, {answer[1]} blood tests"

    print(f"The answer to the {q_number} question is {answer}")

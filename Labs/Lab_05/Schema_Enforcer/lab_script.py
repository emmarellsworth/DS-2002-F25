import csv

rows = [
    ["student_id","major","GPA","is_cs_major","credits_taken"],
    [101,"Computer Science",3,"Yes","15.0"],
    [102,"Biology",3.5,"No","12.5"],
    [103,"Data Science",4,"Yes","18.0"],
    [104,"Mathematics",2,"No","10.5"],
    [105,"Physics",3.25,"No","14"]
]

with open("raw_survey_data.csv","w",newline="") as f:
    csv.writer(f).writerows(rows)

print("wrote raw_survey_data.csv")

import json

courses = [
    {
        "course_id": "DS2002",
        "section": "001",
        "title": "Data Science Systems",
        "level": 200,
        "instructors": [
            {"name": "Austin Rivera", "role": "Primary"},
            {"name": "Heywood Williams-Tracy", "role": "TA"}
        ]
    },
    {
        "course_id": "EVSC3020",
        "section": "100",
        "title": "GIS METHODS",
        "level": 300,
        "instructors": [
            {"name": "John Porter", "role": "Primary"}
        ]
    }
]

with open("raw_course_catalog.json", "w") as f:
    json.dump(courses, f, indent=2)

print("Wrote raw_course_catalog.json with hierarchical data")

import pandas as pd

df = pd.read_csv("raw_survey_data.csv")

df["is_cs_major"] = df["is_cs_major"].replace({
    "Yes": True,
    "No": False
})

df = df.astype({
    "GPA": "float64",
    "credits_taken": "float64"
})

df.to_csv("clean_survey_data.csv", index=False)
print("Cleaned data saved as 'clean_survey_data.csv'")

with open("raw_course_catalog.json") as f:
    data = json.load(f)

df = pd.json_normalize(
    data,
    record_path=["instructors"],
    meta=["course_id", "title", "level"],
)

df.to_csv("clean_course_catalog.csv", index=False)

print("wrote clean_course_catalog.csv")
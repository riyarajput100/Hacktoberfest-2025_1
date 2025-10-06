# bmi_dataset_calculator.py
import pandas as pd

data = {
    "Name": ["Riya", "Aman", "Chetan", "Priya"],
    "Weight_kg": [55, 75, 68, 50],
    "Height_m": [1.6, 1.8, 1.75, 1.55]
}

df = pd.DataFrame(data)
df["BMI"] = df["Weight_kg"] / (df["Height_m"] ** 2)
df["Category"] = pd.cut(
    df["BMI"],
    bins=[0, 18.5, 24.9, 29.9, 100],
    labels=["Underweight", "Normal", "Overweight", "Obese"]
)

print("⚖️ BMI Dataset:")
print(df)

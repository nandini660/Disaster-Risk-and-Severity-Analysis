"""
Disaster Risk Analysis Project

This project analyzes global disaster data from the EM-DAT database to
understand disaster patterns, economic losses, and human impact.

Main steps performed:
1. Data Loading
2. Data Cleaning and Preprocessing
3. Handling Missing Values
4. Feature Engineering
5. Exploratory Data Analysis (EDA)

Key risk indicators created:
- Damage per Affected
- Fatality Rate
- Severity Score
- Disaster Duration
"""

# =====================================
# 1. Import Libraries
# =====================================


import pandas as pd
import numpy as np

# =====================================
# 2. Load Dataset
# =====================================

data = pd.read_excel("C:/Users/Sharma/Downloads/public_emdat_custom_request_2026-03-06_9e76b274-785e-4e65-aedf-75ad25b7ed24.xlsx")

# =========================================================
# 3. Initial Data Exploration
# Understand dataset structure, statistics, and missing values
# =========================================================

print(data.head())
print(data.info())
print(data.describe())
print(data.isnull().sum())

# =========================================================
# 4. Remove Irrelevant Columns
# Columns that are not useful for risk analysis are removed
# =========================================================

drop_cols = [
'DisNo.',
'Historic',
'Classification Key',
'External IDs',
'Event Name',
'Origin',
'Associated Types',
'OFDA/BHA Response',
'Appeal',
'Declaration',
'River Basin',
'Admin Units',
'GADM Admin Units',
'Entry Date',
'Last Update',
'CPI',
"Reconstruction Costs ('000 US$)",
"Reconstruction Costs, Adjusted ('000 US$)",
"No. Homeless",
"AID Contribution ('000 US$)"
]


data = data.drop(columns=drop_cols)


print("\nColumns after drop:")
print(data.columns)

print("\nData info after drop:")
print(data.info())

print("\nMissing values after drop:")
print(data.isnull().sum())

# =========================================================
# 5. Handle Missing Values
# Create indicator variables and fill missing values
# =========================================================

# Create indicator column to track whether damage data was recorded
data['Damage Recorded'] = data["Total Damage ('000 US$)"].notnull().astype(int)
print(data.columns)

# Replace missing total damage values with 0
data["Total Damage ('000 US$)"] = data["Total Damage ('000 US$)"].fillna(0)

print(data[["Total Damage ('000 US$)", "Damage Recorded"]].head())

print(data["Total Damage ('000 US$)"].isna().sum())

print(data.isnull().sum())

# Replace missing location with "Unknown"
data["Location"] = data["Location"].fillna("Unknown")

# Latitude and Longitude have too many missing values → remove them
data = data.drop(columns=["Latitude", "Longitude"])

print(data.isnull().sum())

# Fill missing start date values
data["Start Month"] = data["Start Month"].fillna(data["Start Month"].mode()[0])

data["Start Day"] = data["Start Day"].fillna(data["Start Day"].median()).astype(int)

# Fill missing start date values
data["End Month"] = data["End Month"].fillna(data["End Month"].mode()[0])

data["End Day"] = data["End Day"].fillna(data["End Day"].median()).astype(int)

print(data.isnull().sum())

# Create indicator column for magnitude recording
data["Magnitude Recorded"] = data["Magnitude"].notnull().astype(int)

# Replace missing magnitude values with 0
data["Magnitude"] = data["Magnitude"].fillna(0)

# Replace missing magnitude values with 0
data["Total Deaths"] = data["Total Deaths"].fillna(0)


# Create indicator column for injury data availability
data["Injury Recorded"] = data["No. Injured"].notnull().astype(int)

# Fill missing injured values with -1 to indicate missing data
data["No. Injured"] = data["No. Injured"].fillna(-1)

print(data[["No. Injured","Injury Recorded"]].head())

print(data.isnull().sum())

# Replace missing magnitude scale with "Unknown"
data["Magnitude Scale"] = data["Magnitude Scale"].fillna("Unknown")

# Drop insurance-related columns due to excessive missing values
data = data.drop(columns=[
"Insured Damage ('000 US$)",
"Insured Damage, Adjusted ('000 US$)"
])

# Remove adjusted damage column
data = data.drop(columns=[
"Total Damage, Adjusted ('000 US$)"
])

print(data.isnull().sum())

# Estimate Total Affected when possible
data["Total Affected"] = data["Total Affected"].fillna(
    data["No. Injured"] + data["No. Affected"]
)

# Fill remaining missing affected values using median
data["No. Affected"] = data["No. Affected"].fillna(data["No. Affected"].median())

# Recalculate Total Affected to maintain consistency
data["Total Affected"] = data["No. Injured"] + data["No. Affected"]


print(data.isnull().sum())

# =========================================================
# 6. Feature Engineering
# Create new variables to measure disaster impact
# =========================================================

# ---------------------------------------------------------
# Disaster Duration
# Calculate number of days between start and end of disaster
# ---------------------------------------------------------

data["Start Date"] = pd.to_datetime(
    data[["Start Year","Start Month","Start Day"]].rename(
        columns={
            "Start Year":"year",
            "Start Month":"month",
            "Start Day":"day"
        }
    )
)

data["End Date"] = pd.to_datetime(
    data[["End Year","End Month","End Day"]].rename(
        columns={
            "End Year":"year",
            "End Month":"month",
            "End Day":"day"
        }
    )
)

data["Disaster Duration"] = (data["End Date"] - data["Start Date"]).dt.days

print(data["Disaster Duration"].head(10))

print(data[[
"Start Year","Start Month","Start Day",
"End Year","End Month","End Day"
]].head(10))

# ---------------------------------------------------------
# Damage per Affected Person
# Economic loss per affected individual
# ---------------------------------------------------------

data["Damage per Affected"] = data["Total Damage ('000 US$)"] / data["Total Affected"]

data["Damage per Affected"] = data["Damage per Affected"].replace([float('inf')], 0)

print(data["Damage per Affected"].head())

# ---------------------------------------------------------
# Fatality Rate
# Proportion of affected individuals who died
# ---------------------------------------------------------

# Fatality Rate = Total Deaths / Total Affected

data["Fatality Rate"] = data["Total Deaths"] / data["Total Affected"]

data["Fatality Rate"] = data["Fatality Rate"].replace([float('inf')], 0)

data["Fatality Rate"] = data["Fatality Rate"].fillna(0)

print(data["Fatality Rate"].head())

# ---------------------------------------------------------
# Disaster Severity Score
# Composite risk indicator combining economic and human impact
# ---------------------------------------------------------

# Normalize variables

data["Deaths_norm"] = data["Total Deaths"] / data["Total Deaths"].max()
data["Injured_norm"] = data["No. Injured"] / data["No. Injured"].max()
data["Affected_norm"] = data["Total Affected"] / data["Total Affected"].max()
data["Damage_norm"] = data["Total Damage ('000 US$)"] / data["Total Damage ('000 US$)"].max()

data["Severity Score"] = (
    0.4 * data["Damage_norm"] +
    0.3 * data["Deaths_norm"] +
    0.2 * data["Injured_norm"] +
    0.1 * data["Affected_norm"]
)

print(data["Severity Score"].head())

# ---------------------------------------------------------
# Risk Category based on Severity Score
# Categorizes disasters into risk levels
# ---------------------------------------------------------

def categorize_risk(score):
    if score < 0.25:
        return "Low"
    elif score < 0.50:
        return "Moderate"
    elif score < 0.75:
        return "High"
    else:
        return "Extreme"

data["Risk Category"] = data["Severity Score"].apply(categorize_risk)

print(data[["Severity Score","Risk Category"]].head())

# =========================================================
# 7. Exploratory Data Analysis (EDA)
# Visualizing disaster trends and impacts
# =========================================================


import matplotlib.pyplot as plt

# Group data by disaster type and sum total damage
# ---------------------------------------------------------
# Total Economic Damage by Disaster Type
# ---------------------------------------------------------
damage_by_type = (
    data.groupby("Disaster Type")["Total Damage ('000 US$)"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Create a larger figure
plt.figure(figsize=(12,6))

# Plot bar chart
damage_by_type.plot(kind="bar")

# Titles and labels
plt.title("Total Economic Damage by Disaster Type", fontsize=14)
plt.xlabel("Disaster Type", fontsize=12)
plt.ylabel("Total Damage ('000 US$)", fontsize=12)

# Rotate x-axis labels so they are readable
plt.xticks(rotation=45, ha="right")

# Adjust layout so labels don't get cut
plt.tight_layout()

# Show the chart
plt.show()

# ---------------------------------------------------------
# Average Severity Score by Disaster Type
# ---------------------------------------------------------

# Step 1: Create grouped data
severity_by_type = data.groupby("Disaster Type")["Severity Score"].mean()

# Step 2: Plot
plt.figure(figsize=(10, 6))

severity_by_type.sort_values(ascending=False).head(10).plot(kind="bar")

plt.title("Average Severity Score by Disaster Type")
plt.xlabel("Disaster Type")
plt.ylabel("Severity Score")

plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# Disaster Frequency Over Time
# ---------------------------------------------------------

disasters_per_year = data.groupby("Start Year").size()

disasters_per_year.plot(kind="line")

plt.title("Number of Disasters Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Disasters")

plt.show()

# ---------------------------------------------------------
# Top 10 Most Expensive Disasters
# ---------------------------------------------------------

top_damage = data.sort_values("Total Damage ('000 US$)", ascending=False).head(10)

plt.barh(top_damage["Disaster Type"], top_damage["Total Damage ('000 US$)"])

plt.title("Top 10 Most Expensive Disasters")
plt.xlabel("Total Damage ('000 US$)")
plt.ylabel("Disaster Type")

plt.show()

# ---------------------------------------------------------
# Total Economic Damage by Region
# ---------------------------------------------------------

# Step 1: Group data
damage_by_region = (
    data.groupby("Region")["Total Damage ('000 US$)"]
    .sum()
    .sort_values(ascending=False)
)

# Step 2: Plot
plt.figure(figsize=(12,6))

damage_by_region.plot(kind="bar")

plt.title("Total Economic Damage by Region", fontsize=14)
plt.xlabel("Region", fontsize=12)
plt.ylabel("Total Damage ('000 US$)", fontsize=12)

# Fix label overlapping
plt.xticks(rotation=30, ha="right")

plt.tight_layout()

plt.show()

# ---------------------------------------------------------
# Relationship Between Disaster Magnitude and Fatality Rate
# ---------------------------------------------------------

plt.scatter(data["Magnitude"], data["Fatality Rate"])

plt.title("Magnitude vs Fatality Rate")
plt.xlabel("Magnitude")
plt.ylabel("Fatality Rate")

plt.show()


# =========================================================
# Distribution of Disaster Risk Categories
# =========================================================

data["Risk Category"].value_counts().plot(kind="bar")

plt.title("Distribution of Disaster Risk Categories")
plt.xlabel("Risk Category")
plt.ylabel("Number of Disasters")

plt.tight_layout()
plt.show()






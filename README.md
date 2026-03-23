 **Disaster Risk Analysis**

**Project Overview:**

* This project analyzes global disaster data from the EM-DAT International Disaster Database to understand patterns in disaster occurrence, human impact, and economic losses.

* The goal is to explore disaster trends and develop simple indicators that help measure disaster severity and risk.

**Dataset:**

The dataset comes from the EM-DAT Global Disaster Database and includes worldwide disaster events such as floods, earthquakes, storms, droughts, and wildfires.

**Dataset features include**:

* Disaster type and location
* Start and end dates
* Total deaths and injuries
* Total affected population
* Economic damage estimates

 **Key Steps in the Project:**
1. **Data Cleaning**

* leave empty or put a normal space ;Removed unnecessary columns
* leave empty or put a normal space ;Handled missing values
* leave empty or put a normal space ;Created indicator variables for missing data

**2. Feature Engineering**

   New variables were created to better measure disaster impact:

* Disaster Duration\*\* – time between disaster start and end dates
* Damage per Affected\*\* – economic damage per affected person
* Fatality Rate\*\* – deaths relative to affected population
* Severity Score\*\* – combined indicator based on damage, deaths, injuries, and affected population
* Risk Category\*\* – disasters classified as Low, Moderate, High, or Extreme risk

 3 *Exploratory Data Analysis**
    Several visualizations were created to understand disaster patterns, including:

* Disaster frequency over time
* Economic damage by disaster type
* Average severity by disaster type
* Regional disaster damage
* Relationship between disaster magnitude and fatality rate
* Distribution of disaster risk categories

**Key Insights**

* Disaster frequency has increased over time.
* Floods and storms are among the most common disasters.
* Some regions experience significantly higher economic losses.
* High magnitude disasters tend to produce higher fatality rates.

**Tools Used**

1. Python
2. Pandas
3. NumPy
4. Matplotlib

**Project Structure**

Disaster-Risk-Analysis

1. data

* raw\_disaster\_data.xlsx
* cleaned\_disaster\_data.csv

 2 images

visualization outputs

 3. main.py

* data cleaning, feature engineering, and analysis

 4. README.md

 project documentation

 \# Conclusion:

This project demonstrates how disaster data can be cleaned, analyzed, and visualized to understand global disaster risk patterns. Such analyses are useful for disaster risk assessment and catastrophe risk management.
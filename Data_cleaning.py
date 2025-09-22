import pandas as pd
import numpy as np

# Load the original dataset
df = pd.read_csv('survey.csv')

# List of columns to keep
columns_to_keep = [
    'Age', 'Gender', 'Country', 'self_employed', 'family_history', 'treatment',
    'work_interfere', 'no_employees', 'remote_work', 'tech_company',
    'benefits', 'care_options', 'wellness_program', 'seek_help', 'anonymity',
    'leave', 'mental_health_consequence', 'phys_health_consequence',
    'coworkers', 'supervisor', 'mental_health_interview', 'phys_health_interview',
    'mental_vs_physical', 'obs_consequence'
]

# Select only the columns to keep
df_cleaned = df[columns_to_keep]

# 1. Standardize Gender
def clean_gender(g):
    if pd.isnull(g):
        return "Other"
    g = str(g).strip().lower()
    if g in ['male', 'm', 'man', 'cis male', 'male-ish', 'maile', 'mal', 'make', 'male (cis)', 'cis man']:
        return 'Male'
    elif g in ['female', 'f', 'woman', 'cis female', 'femake', 'female (cis)', 'cis-female/femme', 'female ']:
        return 'Female'
    else:
        return 'Other'

df['Gender'] = df['Gender'].apply(clean_gender)

# 2. Standardize Yes/No fields
yes_no_columns = [
    'self_employed', 'family_history', 'treatment', 'remote_work', 'tech_company',
    'benefits', 'care_options', 'wellness_program', 'seek_help', 'anonymity',
    'mental_health_consequence', 'phys_health_consequence', 'coworkers', 'supervisor',
    'mental_health_interview', 'phys_health_interview', 'mental_vs_physical', 'obs_consequence'
]

def clean_yes_no(val):
    if pd.isnull(val):
        return "No"
    val = str(val).strip().lower()
    if val in ['yes', 'y', '1', 'true']:
        return 'Yes'
    elif val in ['no', 'n', '0', 'false']:
        return 'No'
    else:
        return 'No'  # Default to 'No' for ambiguous values

for col in yes_no_columns:
    if col in df.columns:
        df[col] = df[col].apply(clean_yes_no)

# 3. Standardize company size (no_employees)
def clean_company_size(size):
    if pd.isnull(size):
        return 'Unknown'
    size = str(size).strip().lower()
    if '1-5' in size:
        return '1-5'
    elif '6-25' in size:
        return '6-25'
    elif '26-100' in size:
        return '26-100'
    elif '100-500' in size:
        return '100-500'
    elif '500-1000' in size:
        return '500-1000'
    elif 'more than 1000' in size or '1000+' in size:
        return 'More than 1000'
    else:
        return 'Other'

df['no_employees'] = df['no_employees'].apply(clean_company_size)


# 4. Handle Age column
df['Age'] = df['Age'].apply(lambda x: x if (isinstance(x, (int, float)) and 0 < x <= 100) else np.nan)

# 5. Handle missing/invalid values in critical fields
critical_fields = ['Gender', 'Country', 'no_employees']
for col in critical_fields:
    df[col] = df[col].fillna('Unknown')
    df[col] = df[col].replace(['NA', 'N/A', 'na', 'n/a', '', 'Not sure', "Don't know"], 'Unknown')

# 6. For categorical columns, replace NA/Not sure/Don't know with 'Unknown'
categorical_columns = [
    'self_employed', 'family_history', 'treatment', 'work_interfere', 'remote_work', 'tech_company',
    'benefits', 'care_options', 'wellness_program', 'seek_help', 'anonymity', 'leave',
    'mental_health_consequence', 'phys_health_consequence', 'coworkers', 'supervisor',
    'mental_health_interview', 'phys_health_interview', 'mental_vs_physical', 'obs_consequence'
]
for col in categorical_columns:
    if col in df.columns:
        df[col] = df[col].fillna('Unknown')
        df[col] = df[col].replace(['NA', 'N/A', 'na', 'n/a', '', 'Not sure', "Don't know"], 'Unknown')

# 7. Convert Age to integer (nullable)
df['Age'] = pd.to_numeric(df['Age'], errors='coerce').astype('Int64')

# 8. List of Yes/No fields to convert
boolean_columns = [
    'self_employed', 'family_history', 'treatment', 'remote_work', 'tech_company',
    'benefits', 'care_options', 'wellness_program', 'seek_help', 'anonymity', 'leave',
    'mental_health_consequence', 'phys_health_consequence', 'coworkers', 'supervisor',
    'mental_health_interview', 'phys_health_interview', 'mental_vs_physical', 'obs_consequence'
]

def yes_no_to_int(val):
    if val == 'Yes':
        return 1
    elif val == 'No':
        return 0
    else:
        return None  # For 'Unknown' or other values

for col in boolean_columns:
    if col in df.columns:
        df[col] = df[col].apply(yes_no_to_int).astype('Int64')

# If you have a Timestamp column:
# df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.date

# Save the final, typed dataset
df.to_csv('survey_final_typed.csv', index=False)

import pandas as pd

# Load the dataset
df = pd.read_csv('NEVO2023_8.0_clean.csv')

# Find the vitamin C content in 100 grams of white asparagus
white_asparagus_vitamin_c = df[df['Voedingsmiddelnaam/Dutch food name'] == 'Asperge witte rauw']['VITC (mg)'].iloc[0]

# Calculate the vitamin C content in 200 grams
vitamin_c_200g = white_asparagus_vitamin_c * 2

# Print the vitamin C content in 200 grams
print(f'The vitamin C content in 200 grams of raw white asparagus is {vitamin_c_200g} mg.')

# Determine how much of the daily vitamin C requirement is fulfilled
daily_required_vitamin_c_men = 90 # mg; daily_required_vitamin_c_women = 75 mg

# Assuming the person is a man, we use the higher value for calculation.
daily_required_vitamin_c = daily_required_vitamin_c_men

# Calculate the percentage fulfilled
percentage_fulfilled = (vitamin_c_200g / daily_required_vitamin_c) * 100

# Print the percentage fulfilled
print(f'The consumption of 200 grams of raw white asparagus fulfills {percentage_fulfilled}% of the daily vitamin C requirement.')

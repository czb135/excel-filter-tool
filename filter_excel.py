import pandas as pd

# Read the Excel file
df = pd.read_excel('test.xlsx')

# Display the first few rows to understand the structure
print("Original data shape:", df.shape)
print("\nFirst few rows:")
print(df.head())
print("\nColumn names:")
print(df.columns.tolist())

# Filter the data based on service_number criteria
# service_number is 180992, 180993, or between 181011 and 181068
filtered_df = df[
    (df['service_number'] == 180992) |
    (df['service_number'] == 180993) |
    ((df['service_number'] >= 181011) & (df['service_number'] <= 181068))
]

print(f"\nFiltered data shape: {filtered_df.shape}")
print("\nFiltered rows:")
print(filtered_df)

# Extract column B "tno" from filtered data
tno_column = filtered_df['tno']

# Create output DataFrame with filter name
output_df = pd.DataFrame({
    'NJ600': tno_column.values
})

# Save to Excel file
output_filename = 'NJ600_filtered.xlsx'
output_df.to_excel(output_filename, index=False)

print(f"\nFiltered 'tno' column saved to {output_filename}")
print(f"\nOutput data:")
print(output_df)


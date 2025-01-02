import pandas as pd

df = pd.read_csv("output_etext_transcripts.csv")

# Sort the Dataframe by file_name column in ascending order
sorted_df = df.sort_values(by="file_name", ascending=True)
# Write the sorted Dataframe to a new CSV file
sorted_df.to_csv("sorted_output_etext_transcripts.csv", index=False)

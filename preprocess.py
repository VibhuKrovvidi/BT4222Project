import pandas as pd
import regex as re


# Read in dataframe
df = pd.read_csv("scraped_output.csv", index_col=0)

# Remove null reviews
df = df.dropna()

# Tokenize sentence
clean = df.copy()
clean["Reviews"] = clean["Reviews"].str.split(".")

# Convert each word to lowercase
clean["Reviews"] = clean["Reviews"].apply(lambda x: [i.lower() for i in x])

# Remove any special characters:
clean["Reviews"] = clean["Reviews"].apply(lambda x: [re.sub('[^A-Za-z0-9 ]+', '', i) for i in x])
clean["Reviews"] = clean["Reviews"].apply(lambda x: [i for i in x if i!=""])

clean.to_csv("cleaned_data.csv")
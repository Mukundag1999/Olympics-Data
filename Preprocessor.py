import pandas as pd

df= pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

def preprocess():
    global df, region_df

    # Filter for Summer Olympics
    df = df[df['Season'] == 'Summer']

    # Merge with region data
    df = df.merge(region_df, on="NOC", how="left", suffixes=('', '_region'))

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # One-hot encode the medals
    onehot = pd.get_dummies(df['Medal']).astype(int)
    onehot = onehot[['Gold', 'Silver', 'Bronze']]  # Ensure only relevant columns are kept
    df = pd.concat([df, onehot], axis=1)

    # Remove duplicate columns if any exist
    df = df.loc[:, ~df.columns.duplicated()]


    return df




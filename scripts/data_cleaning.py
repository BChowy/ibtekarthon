# data_cleaning.py
import pandas as pd
import numpy as np

def clean_landslide_data(raw_url):
    # Load raw data
    df = pd.read_csv(raw_url)
    
    # Keep essential columns
    cols_to_keep = [
        'event_date', 'location_description', 'latitude', 'longitude',
        'landslide_category', 'landslide_size', 'landslide_trigger',
        'fatality_count', 'injury_count'
    ]
    df = df[cols_to_keep].copy()
    
    # Rename columns to match your dashboard
    df = df.rename(columns={
        'fatality_count': 'fatality_count',
        'injury_count': 'injury_count'
    })
    
    # Clean numerical values
    df['fatality_count'] = (
        pd.to_numeric(df['fatality_count'], errors='coerce')
        .fillna(0)
        .astype(int)
    )
    
    df['injury_count'] = (
        pd.to_numeric(df['injury_count'], errors='coerce')
        .fillna(0)
        .astype(int)
    )
    
    # Clean coordinates
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df = df.dropna(subset=['latitude', 'longitude'])
    
    # Clean dates
    df['event_date'] = pd.to_datetime(df['event_date'], errors='coerce')
    df = df.dropna(subset=['event_date'])
    
    # Clean categorical data
    df['landslide_category'] = (
        df['landslide_category']
        .str.lower()
        .str.replace(' ', '_')
        .fillna('unknown')
    )
    
    df['landslide_size'] = (
        df['landslide_size']
        .str.lower()
        .str.replace(' ', '_')
        .fillna('unknown')
    )
    
    df['landslide_trigger'] = (
        df['landslide_trigger']
        .str.lower()
        .str.replace(' ', '_')
        .fillna('unknown')
    )
    
    # Filter categories to match your dashboard
    valid_categories = ['landslide', 'mudslide', 'rock_fall']
    df = df[df['landslide_category'].isin(valid_categories)]
    
    valid_sizes = ['small', 'medium', 'large']
    df = df[df['landslide_size'].isin(valid_sizes)]
    
    # Final cleaning
    df = df.reset_index(drop=True)
    df = df.drop_duplicates()
    
    return df

if __name__ == "__main__":
    # NASA raw data URL
    RAW_URL = "./data/raw_landslide_data.csv"
    
    # Clean and save data
    cleaned_df = clean_landslide_data(RAW_URL)
    cleaned_df.to_csv("data/cleaned_landslide_data2.csv", index=False)
    print("✅ Saved cleaned data to: data/cleaned_landslide_data.csv")
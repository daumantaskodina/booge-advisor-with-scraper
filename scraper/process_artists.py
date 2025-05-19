import csv
import json
import os
from datetime import datetime
import pandas as pd
import numpy as np

def extract_artists_from_events(events_csv_path):
    """
    Extract unique artists from events CSV and create an artist-focused dataset
    """
    # Read the events CSV file
    df = pd.read_csv(events_csv_path)
    
    # Check if the 'Artists' column exists
    if 'Artists' not in df.columns:
        print(f"Error: 'Artists' column not found in the CSV file: {events_csv_path}")
        print(f"Available columns: {df.columns.tolist()}")
        return pd.DataFrame()  # Return empty DataFrame
    
    # Extract all artists
    all_artists = []
    
    for _, row in df.iterrows():
        # Handle artists field which might contain comma-separated values
        # Check if the artist field is missing or NaN
        if pd.isna(row['Artists']) or row['Artists'] == '':
            continue
            
        # Convert to string if it's not already (handle numeric values)
        artists_str = str(row['Artists'])
        
        # Remove any quotes if present
        artists_str = artists_str.strip('"')
        
        # Split by comma and strip whitespace
        artists = [artist.strip() for artist in artists_str.split(',')]
        
        # Store artist information
        for artist in artists:
            # Skip empty artist names
            if not artist:
                continue
                
            # Create artist entry with event context
            event_entry = {
                'name': artist,
                'event_name': row['Event name'] if 'Event name' in row and not pd.isna(row['Event name']) else 'Unknown',
                'venue': row['Venue'] if 'Venue' in row and not pd.isna(row['Venue']) else 'Unknown',
                'date': row['Date'] if 'Date' in row and not pd.isna(row['Date']) else 'Unknown',
                'event_url': row['Event URL'] if 'Event URL' in row and not pd.isna(row['Event URL']) else ''
            }
            
            all_artists.append(event_entry)
    
    # If we didn't extract any artists, return empty DataFrame
    if not all_artists:
        print("No artists found in the events data.")
        return pd.DataFrame()
        
    # Create a DataFrame for all artist appearances
    artists_df = pd.DataFrame(all_artists)
    
    # Create a unique artists DataFrame
    unique_artists = artists_df['name'].unique()
    
    # Create comprehensive artist profiles
    artist_profiles = []
    
    for artist_name in unique_artists:
        # Get all events for this artist
        artist_events = artists_df[artists_df['name'] == artist_name]
        
        # Get a valid RA URL
        ra_urls = [f"https://ra.co{url}" for url in artist_events['event_url'] if isinstance(url, str) and url]
        ra_url = ra_urls[0] if ra_urls else ""
        
        # Collect all event names this artist is playing at
        event_names = artist_events['event_name'].tolist()
        
        # Create artist profile with PRD-defined attributes
        artist_profile = {
            'name': artist_name,
            'resident_advisor_url': ra_url,
            'appearances': len(artist_events),
            'events': ', '.join(event_names),  # Added event names
            'venues': ', '.join(artist_events['venue'].unique()),
            'latest_event': artist_events['date'].iloc[0],  # Using first event as reference
            
            # Placeholders for dimensions (0.0-1.0 scale)
            'energy': '',          # Low energy to high energy
            'experimental': '',    # Mainstream to experimental
            'melodic': '',         # Rhythmic to melodic
            'dark': '',            # Light to dark
            'organic': '',         # Digital to organic
            'vocal': '',           # Instrumental to vocal
            'depth': '',           # Surface-level to deep
            'classic': '',         # Modern to classic
            
            # Placeholders for weighted genre, scene, and mood associations
            'genres': '',          # e.g., "Techno:0.8, House:0.4, Minimal:0.3"
            'scenes': '',          # e.g., "Berlin Techno:0.9, Detroit Techno:0.3"
            'moods': '',           # e.g., "Dark:0.7, Hypnotic:0.8"
            
            # Additional fields that could be filled by AI
            'description': '',
            'similar_artists': '',
            'soundcloud_url': '',
            'spotify_id': ''
        }
        
        artist_profiles.append(artist_profile)
    
    # Create DataFrame from artist profiles
    profiles_df = pd.DataFrame(artist_profiles)
    
    return profiles_df

def save_artist_data(artists_df, output_path):
    """
    Save artist data to CSV file
    """
    if artists_df.empty:
        print(f"No artist data to save.")
        return
        
    artists_df.to_csv(output_path, index=False)
    print(f"Saved {len(artists_df)} unique artists to {output_path}")

def main():
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Default input file (most recent events CSV)
    input_files = [f for f in os.listdir(data_dir) if f.endswith('.csv') and f.startswith('berlin_events')]
    if not input_files:
        print("No event CSV files found in the data directory. Please run the event scraper first.")
        return
    
    # Use the most recent file based on modified time
    input_files.sort(key=lambda x: os.path.getmtime(os.path.join(data_dir, x)), reverse=True)
    input_file = os.path.join(data_dir, input_files[0])
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d')
    output_file = os.path.join(data_dir, f'artist_profiles_{timestamp}.csv')
    
    print(f"Processing events from: {input_file}")
    
    # Extract artists and create profiles
    artists_df = extract_artists_from_events(input_file)
    
    if not artists_df.empty:
        # Save to CSV
        save_artist_data(artists_df, output_file)
        print(f"Artist profiles created successfully with placeholders for AI enrichment")
        print(f"Next steps: Enrich these profiles with AI to fill the dimension values and other attributes")
    else:
        print("Could not create artist profiles. Please check the event data format.")

if __name__ == "__main__":
    main() 
import pandas as pd
import os
import random
import sys
import json
from datetime import datetime

def load_artist_profiles(csv_path):
    """
    Load artist profiles from CSV file
    """
    if not os.path.exists(csv_path):
        print(f"Error: File not found: {csv_path}")
        sys.exit(1)
        
    try:
        return pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        sys.exit(1)

def save_artist_profiles(df, output_path):
    """
    Save artist profiles to CSV file
    """
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} enriched artist profiles to {output_path}")

def generate_placeholder_data():
    """
    Generate placeholder data to demonstrate format for AI enrichment
    NOTE: This is just for demonstration and should be replaced with actual AI-generated values
    """
    return {
        'energy': round(random.uniform(0.0, 1.0), 2),
        'experimental': round(random.uniform(0.0, 1.0), 2),
        'melodic': round(random.uniform(0.0, 1.0), 2),
        'dark': round(random.uniform(0.0, 1.0), 2),
        'organic': round(random.uniform(0.0, 1.0), 2),
        'vocal': round(random.uniform(0.0, 1.0), 2),
        'depth': round(random.uniform(0.0, 1.0), 2),
        'classic': round(random.uniform(0.0, 1.0), 2),
        'genres': "Techno:0.8, House:0.4, Minimal:0.3",
        'scenes': "Berlin Techno:0.9, Detroit Techno:0.3",
        'moods': "Dark:0.7, Hypnotic:0.8",
        'description': "This artist is known for deep, hypnotic techno with industrial influences.",
        'similar_artists': "Artist1, Artist2, Artist3",
        'soundcloud_url': "https://soundcloud.com/example",
        'spotify_id': "spotify:artist:123456789"
    }

def export_template_for_ai(df, output_path):
    """
    Export a JSON template that can be used for AI enrichment
    """
    # Create a list of artist entries with basic info and placeholders
    artists_data = []
    for _, row in df.iterrows():
        artist_entry = {
            'name': row['name'],
            'event_context': {
                'events': row['events'] if 'events' in row else '',  # Added events field
                'venues': row['venues'],
                'appearances': row['appearances'],
                'latest_event': row['latest_event'],
                'resident_advisor_url': row['resident_advisor_url']
            },
            'dimensions': {
                'energy': None,          # 0.0-1.0 scale: Low energy to high energy
                'experimental': None,    # 0.0-1.0 scale: Mainstream to experimental
                'melodic': None,         # 0.0-1.0 scale: Rhythmic to melodic
                'dark': None,            # 0.0-1.0 scale: Light to dark
                'organic': None,         # 0.0-1.0 scale: Digital to organic
                'vocal': None,           # 0.0-1.0 scale: Instrumental to vocal
                'depth': None,           # 0.0-1.0 scale: Surface-level to deep
                'classic': None          # 0.0-1.0 scale: Modern to classic
            },
            'associations': {
                'genres': None,          # e.g., {"Techno": 0.8, "House": 0.4, "Minimal": 0.3}
                'scenes': None,          # e.g., {"Berlin Techno": 0.9, "Detroit Techno": 0.3}
                'moods': None            # e.g., {"Dark": 0.7, "Hypnotic": 0.8}
            },
            'metadata': {
                'description': None,
                'similar_artists': None,
                'soundcloud_url': None,
                'spotify_id': None
            }
        }
        artists_data.append(artist_entry)
    
    # Save to JSON file
    with open(output_path, 'w') as f:
        json.dump(artists_data, f, indent=2)
    
    print(f"Exported AI enrichment template for {len(artists_data)} artists to {output_path}")
    print("This template can be processed by AI to fill in the missing values")

def import_ai_enriched_data(csv_path, json_path, output_path):
    """
    Import AI-enriched data from JSON file and merge with original CSV
    """
    # Load original CSV
    df = load_artist_profiles(csv_path)
    
    # Load enriched JSON
    try:
        with open(json_path, 'r') as f:
            enriched_data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)
    
    # Create a dictionary mapping artist names to their enriched data
    enriched_dict = {}
    for artist in enriched_data:
        name = artist['name']
        
        # Extract data from the nested structure
        dimensions = artist['dimensions']
        associations = artist['associations']
        metadata = artist['metadata']
        
        # Convert associations to string format for CSV
        genres_str = ", ".join([f"{k}:{v}" for k, v in associations['genres'].items()]) if associations['genres'] else ""
        scenes_str = ", ".join([f"{k}:{v}" for k, v in associations['scenes'].items()]) if associations['scenes'] else ""
        moods_str = ", ".join([f"{k}:{v}" for k, v in associations['moods'].items()]) if associations['moods'] else ""
        
        # Create entry with all enriched data
        enriched_dict[name] = {
            'energy': dimensions['energy'],
            'experimental': dimensions['experimental'],
            'melodic': dimensions['melodic'],
            'dark': dimensions['dark'],
            'organic': dimensions['organic'],
            'vocal': dimensions['vocal'],
            'depth': dimensions['depth'],
            'classic': dimensions['classic'],
            'genres': genres_str,
            'scenes': scenes_str,
            'moods': moods_str,
            'description': metadata['description'],
            'similar_artists': ", ".join(metadata['similar_artists']) if metadata['similar_artists'] else "",
            'soundcloud_url': metadata['soundcloud_url'],
            'spotify_id': metadata['spotify_id']
        }
    
    # Update the DataFrame with enriched data
    for i, row in df.iterrows():
        name = row['name']
        if name in enriched_dict:
            for field, value in enriched_dict[name].items():
                df.at[i, field] = value
    
    # Save the enriched DataFrame
    save_artist_profiles(df, output_path)
    
    return df

def main():
    # Command line arguments
    if len(sys.argv) < 2:
        print("Usage:")
        print("  To generate an AI template:  python enrich_artists.py --generate-template [input_csv]")
        print("  To import AI enriched data:  python enrich_artists.py --import-enriched [input_csv] [enriched_json]")
        print("  To fill with random values:  python enrich_artists.py --demo [input_csv]")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Get the most recent artist profile CSV if not specified
    if len(sys.argv) > 2:
        input_csv = sys.argv[2]
    else:
        input_files = [f for f in os.listdir(data_dir) if f.endswith('.csv') and f.startswith('artist_profiles')]
        if not input_files:
            print("No artist profile CSV files found in the data directory.")
            print("Please run process_artists.py first.")
            sys.exit(1)
        
        # Use the most recent file based on modified time
        input_files.sort(key=lambda x: os.path.getmtime(os.path.join(data_dir, x)), reverse=True)
        input_csv = os.path.join(data_dir, input_files[0])
    
    # Make sure input_csv path is complete
    if not os.path.isabs(input_csv):
        input_csv = os.path.join(data_dir, input_csv)
    
    # Generate timestamp for output files
    timestamp = datetime.now().strftime('%Y-%m-%d')
    
    if mode == "--generate-template":
        # Load artist profiles
        df = load_artist_profiles(input_csv)
        
        # Export template for AI enrichment
        output_json = os.path.join(data_dir, f'ai_template_{timestamp}.json')
        export_template_for_ai(df, output_json)
        
    elif mode == "--import-enriched":
        if len(sys.argv) < 4:
            print("Error: Please provide the path to the enriched JSON file.")
            sys.exit(1)
            
        enriched_json = sys.argv[3]
        if not os.path.isabs(enriched_json):
            enriched_json = os.path.join(data_dir, enriched_json)
            
        output_csv = os.path.join(data_dir, f'enriched_artists_{timestamp}.csv')
        
        # Import and merge enriched data
        import_ai_enriched_data(input_csv, enriched_json, output_csv)
        
    elif mode == "--demo":
        # Load artist profiles
        df = load_artist_profiles(input_csv)
        
        # Fill with random placeholder values
        print("Filling with random placeholder values for demonstration...")
        for i, _ in df.iterrows():
            placeholder = generate_placeholder_data()
            for field, value in placeholder.items():
                df.at[i, field] = value
        
        # Save enriched profiles
        output_csv = os.path.join(data_dir, f'demo_enriched_artists_{timestamp}.csv')
        save_artist_profiles(df, output_csv)
        
        print("Note: These are randomly generated values for demonstration only.")
        print("      In a real scenario, these would be generated by AI based on artist analysis.")
    
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
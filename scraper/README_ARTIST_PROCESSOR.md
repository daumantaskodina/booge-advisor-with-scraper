# Artist Data Processor for BOOGEY ADVISOR

This component extracts artist data from scraped Resident Advisor events and prepares it for AI enrichment with the musical attributes defined in the BOOGEY ADVISOR PRD.

## Overview

The workflow is designed to:

1. Extract unique artists from event data
2. Create an initial CSV with artist profiles and placeholder attributes
3. Generate a template for AI enrichment
4. Import AI-enriched data and create a final artist dataset

## Key Components

- `process_artists.py`: Extracts unique artists from event data
- `extract_artists.sh`: Shell script for easy execution
- `enrich_artists.py`: Tools for AI enrichment workflow

## Usage

### 1. Extract Artists from Events

First, you need to have event data. If you haven't scraped events yet, run:

```bash
./fetch_berlin_events.sh
```

Then extract the artists:

```bash
./extract_artists.sh
```

Alternatively, you can do both steps at once:

```bash
./extract_artists.sh --scrape-first [START_DATE] [END_DATE]
```

This will create a CSV file in the `data` directory named `artist_profiles_YYYY-MM-DD.csv`.

### 2. Generate AI Enrichment Template

To prepare a template for AI enrichment:

```bash
python enrich_artists.py --generate-template
```

This creates a JSON file in the `data` directory with the format that needs to be filled by AI.

### 3. Enrich with AI

The JSON template should be processed by an AI (like Claude, GPT-4, etc.) to fill in the attributes for each artist. The AI should analyze each artist based on their style and fill in values for:

- **Dimensions** (0.0-1.0 scale):
  - Energy (low energy to high energy)
  - Experimental (mainstream to experimental)
  - Melodic (rhythmic to melodic)
  - Dark (light to dark)
  - Organic (digital to organic)
  - Vocal (instrumental to vocal)
  - Depth (surface-level to deep) 
  - Classic (modern to classic)

- **Associations**:
  - Genres (with weights, e.g., {"Techno": 0.8, "House": 0.4})
  - Scenes (e.g., {"Berlin Techno": 0.9})
  - Moods (e.g., {"Dark": 0.7, "Hypnotic": 0.8})

- **Metadata**:
  - Description
  - Similar artists
  - SoundCloud URL (if available)
  - Spotify ID (if available)

### 4. Import Enriched Data

Once you have the AI-enriched JSON file, import it:

```bash
python enrich_artists.py --import-enriched [input_csv] [enriched_json]
```

This merges the AI-generated attributes with the original artist profiles.

### 5. Demo Mode (Optional)

For testing the workflow, you can fill the attributes with random values:

```bash
python enrich_artists.py --demo
```

This creates a demo file with random values just to show the format.

## Output Data Structure

The final enriched CSV file includes:

- **Basic info**: 
  - Artist name
  - Event names (all events the artist is playing at)
  - RA URL
  - Venues
  - Appearances

- **Dimensions**: All eight numerical attributes (0.0-1.0)
- **Associations**: Genres, scenes, and moods with weights
- **Metadata**: Description and links

## Next Steps

After creating this enriched artist dataset, you can:

1. Use it in the recommendation engine to match user preferences with artists
2. Integrate it with the BOOGEY ADVISOR frontend
3. Periodically update artist data as new events are scraped 
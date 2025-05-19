#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Check if we need to run the event scraper first
if [ "$1" == "--scrape-first" ]; then
  # Get date parameters or use defaults (next 7 days)
  START_DATE=${2:-$(date +%Y-%m-%d)}
  END_DATE=${3:-$(date -v+7d +%Y-%m-%d)}
  OUTPUT_FILE=${4:-"../data/berlin_events.csv"}
  
  echo "Fetching Berlin events from $START_DATE to $END_DATE..."
  python event_fetcher.py 34 "$START_DATE" "$END_DATE" -o "$OUTPUT_FILE"
  
  if [ $? -ne 0 ]; then
    echo "Error running event scraper. Aborting."
    exit 1
  fi
fi

# Process artists
echo "Extracting artist profiles..."
python process_artists.py

echo ""
echo "To enrich these artist profiles with AI data, use the data files in the data directory." 
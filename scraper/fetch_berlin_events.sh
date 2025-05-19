#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Get date parameters or use defaults (next 7 days)
START_DATE=${1:-$(date +%Y-%m-%d)}
END_DATE=${2:-$(date -v+7d +%Y-%m-%d)}
OUTPUT_FILE=${3:-"../data/berlin_events.csv"}

# Create data directory if it doesn't exist
mkdir -p ../data

# Run the scraper
echo "Fetching Berlin events from $START_DATE to $END_DATE..."
python event_fetcher.py 34 "$START_DATE" "$END_DATE" -o "$OUTPUT_FILE"

echo "Events saved to $OUTPUT_FILE"
echo "Found $(wc -l < "$OUTPUT_FILE" | xargs) events (including header row)" 
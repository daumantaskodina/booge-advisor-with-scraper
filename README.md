# BOOGEY ADVISOR with Event Scraper

This project includes a Resident Advisor event scraper component that allows you to fetch electronic music events in Berlin for your BOOGEY ADVISOR app.

## Scraper Component

The scraper uses Python to fetch event data from Resident Advisor's GraphQL API, which is more reliable than traditional HTML scraping and less likely to be detected as a bot.

### Features

- Fetches Berlin electronic music events for a specified date range
- Extracts event details including:
  - Event name
  - Date and time
  - Artists lineup
  - Venue
  - Event URL
  - Number of attendees

### Setup Instructions

1. **Install Python Dependencies**

```bash
cd scraper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Run the Scraper Directly (CLI)**

```bash
cd scraper
./fetch_berlin_events.sh [START_DATE] [END_DATE] [OUTPUT_FILE]
```

For example:
```bash
./fetch_berlin_events.sh 2025-05-19 2025-05-25 ../data/events.csv
```

If no parameters are provided, it will fetch events for the next 7 days.

3. **Using the Next.js Integration**

The scraper is integrated into the Next.js app through:

- A TypeScript module (`src/lib/event-scraper.ts`) for calling the Python scraper
- An API route (`/api/scrape-events`) for triggering the scraper from the frontend
- A React component (`EventScraperTrigger`) for the user interface

Visit `/scraper` in the app to access the scraper UI.

### Technical Notes

- The scraper uses area code 34 for Berlin
- The output is saved as a CSV file
- Each request respects rate limiting to avoid being blocked

## Next Steps

- Implement the artist labeling system according to the PRD
- Build the recommendation engine
- Integrate the scraped events into the user interface 
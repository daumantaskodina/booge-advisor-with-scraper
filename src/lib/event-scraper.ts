import { exec } from 'child_process';
import path from 'path';
import fs from 'fs';
import { promisify } from 'util';

const execAsync = promisify(exec);

interface ScraperOptions {
  startDate?: string; // Format: YYYY-MM-DD
  endDate?: string; // Format: YYYY-MM-DD
  outputFile?: string;
}

interface EventData {
  eventName: string;
  date: string;
  startTime: string;
  endTime: string;
  artists: string[];
  venue: string;
  eventUrl: string;
  attendingCount: number;
}

/**
 * Scrapes Berlin events from Resident Advisor for the given date range
 */
export async function scrapeBerlinEvents(options: ScraperOptions = {}): Promise<EventData[]> {
  try {
    const startDate = options.startDate || new Date().toISOString().split('T')[0];
    const endDate = options.endDate || new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    const outputFile = options.outputFile || path.join(process.cwd(), 'data', 'berlin_events.csv');
    
    // Ensure the data directory exists
    const dataDir = path.dirname(outputFile);
    if (!fs.existsSync(dataDir)) {
      fs.mkdirSync(dataDir, { recursive: true });
    }
    
    // Path to the scraper script - adjust if necessary
    const scraperDir = path.join(process.cwd(), 'scraper');
    
    // Execute the scraper script
    console.log(`Scraping Berlin events from ${startDate} to ${endDate}...`);
    await execAsync(`cd ${scraperDir} && ./fetch_berlin_events.sh "${startDate}" "${endDate}" "${outputFile}"`);
    
    // Read and parse the CSV file
    const csvData = fs.readFileSync(outputFile, 'utf-8');
    const lines = csvData.split('\n');
    
    // Skip the header row and parse the data
    const events: EventData[] = lines.slice(1)
      .filter(line => line.trim().length > 0)
      .map(line => {
        const columns = line.split(',');
        // Handle cases where artist names might contain commas
        let artistsIndex = 4;
        let venueIndex = 5;
        let urlIndex = 6;
        let attendingIndex = 7;
        
        // Adjust indexes if there are quoted fields with commas
        if (columns.length > 8) {
          let tempLine = line;
          let inQuotes = false;
          let commaCount = 0;
          let artistsField = '';
          
          for (let i = 0; i < tempLine.length; i++) {
            if (tempLine[i] === '"') {
              inQuotes = !inQuotes;
            } else if (tempLine[i] === ',' && !inQuotes) {
              commaCount++;
              if (commaCount === 4) {
                // We've found the start of the artists field
                artistsField = tempLine.substring(i + 1);
                break;
              }
            }
          }
          
          // If we found a quoted artists field, extract the venue, URL, and attending count
          if (artistsField) {
            const remainingFields = artistsField.split(',');
            // The artists field is the first element, which may be quoted
            // Find where the quotes end for the artists field
            let artistsEndIndex = 0;
            inQuotes = false;
            for (let i = 0; i < artistsField.length; i++) {
              if (artistsField[i] === '"') {
                inQuotes = !inQuotes;
                if (!inQuotes) {
                  artistsEndIndex = i;
                  break;
                }
              }
            }
            
            if (artistsEndIndex > 0) {
              // Extract the remaining fields after the artists field
              const venue = remainingFields[remainingFields.length - 3];
              const url = remainingFields[remainingFields.length - 2];
              const attending = remainingFields[remainingFields.length - 1];
              
              // Extract the artists field (removing quotes)
              const artists = artistsField.substring(0, artistsEndIndex + 1).replace(/"/g, '');
              
              return {
                eventName: columns[0],
                date: columns[1],
                startTime: columns[2],
                endTime: columns[3],
                artists: artists.split(', '),
                venue,
                eventUrl: url,
                attendingCount: parseInt(attending, 10) || 0
              };
            }
          }
        }
        
        // Fallback to simpler parsing if the complex logic fails
        return {
          eventName: columns[0],
          date: columns[1],
          startTime: columns[2],
          endTime: columns[3],
          artists: columns[artistsIndex].split(', '),
          venue: columns[venueIndex],
          eventUrl: columns[urlIndex],
          attendingCount: parseInt(columns[attendingIndex], 10) || 0
        };
      });
    
    console.log(`Scraped ${events.length} events from Resident Advisor`);
    return events;
    
  } catch (error) {
    console.error('Error scraping Berlin events:', error);
    throw error;
  }
}

/**
 * Example of how to use this function in a Next.js API route or Server Action
 */
export async function fetchLatestEvents(): Promise<EventData[]> {
  const startDate = new Date().toISOString().split('T')[0];
  const endDate = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
  
  return await scrapeBerlinEvents({
    startDate,
    endDate,
    outputFile: path.join(process.cwd(), 'data', `berlin_events_${startDate}_${endDate}.csv`)
  });
} 
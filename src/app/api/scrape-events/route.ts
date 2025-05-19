import { NextResponse } from 'next/server';
import { scrapeBerlinEvents } from '@/lib/event-scraper';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const startDate = searchParams.get('startDate') || undefined;
    const endDate = searchParams.get('endDate') || undefined;
    
    const events = await scrapeBerlinEvents({
      startDate,
      endDate,
    });
    
    return NextResponse.json({ 
      success: true, 
      events,
      count: events.length,
      message: `Successfully scraped ${events.length} events from Resident Advisor` 
    });
  } catch (error) {
    console.error('Error in event scraping API:', error);
    return NextResponse.json(
      { 
        success: false, 
        message: 'Failed to scrape events', 
        error: error instanceof Error ? error.message : String(error) 
      },
      { status: 500 }
    );
  }
} 
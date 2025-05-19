import { EventScraperTrigger } from '@/components/event-scraper-trigger';

export default function ScraperPage() {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-8">RA Event Scraper</h1>
      <EventScraperTrigger />
    </div>
  );
} 
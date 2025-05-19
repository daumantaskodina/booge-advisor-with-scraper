'use client';

import { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';

type Event = {
  eventName: string;
  date: string;
  startTime: string;
  endTime: string;
  artists: string[];
  venue: string;
  eventUrl: string;
  attendingCount: number;
};

export function EventScraperTrigger() {
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [events, setEvents] = useState<Event[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const handleScrape = async () => {
    setIsLoading(true);
    setError(null);
    setMessage(null);

    try {
      const params = new URLSearchParams();
      if (startDate) params.append('startDate', startDate);
      if (endDate) params.append('endDate', endDate);

      const response = await fetch(`/api/scrape-events?${params.toString()}`);
      const data = await response.json();

      if (!data.success) {
        throw new Error(data.message || 'Failed to scrape events');
      }

      setEvents(data.events || []);
      setMessage(data.message);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
      setEvents([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Berlin Event Scraper</CardTitle>
          <CardDescription>
            Scrape electronic music events from Resident Advisor
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="startDate">Start Date</Label>
                <Input
                  id="startDate"
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  placeholder="YYYY-MM-DD"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="endDate">End Date</Label>
                <Input
                  id="endDate"
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  placeholder="YYYY-MM-DD"
                />
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <Button onClick={handleScrape} disabled={isLoading}>
            {isLoading ? 'Scraping...' : 'Scrape Events'}
          </Button>
        </CardFooter>
      </Card>

      {error && (
        <Card className="border-red-500">
          <CardHeader>
            <CardTitle className="text-red-500">Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p>{error}</p>
          </CardContent>
        </Card>
      )}

      {message && (
        <Card className="border-green-500">
          <CardHeader>
            <CardTitle className="text-green-500">Success</CardTitle>
          </CardHeader>
          <CardContent>
            <p>{message}</p>
          </CardContent>
        </Card>
      )}

      {events.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Scraped Events</CardTitle>
            <CardDescription>
              Found {events.length} events from Resident Advisor
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="max-h-96 overflow-y-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="border-b">
                    <th className="p-2 text-left">Event Name</th>
                    <th className="p-2 text-left">Date</th>
                    <th className="p-2 text-left">Venue</th>
                    <th className="p-2 text-left">Artists</th>
                    <th className="p-2 text-right">Attending</th>
                  </tr>
                </thead>
                <tbody>
                  {events.map((event, index) => (
                    <tr key={index} className="border-b">
                      <td className="p-2">
                        <a 
                          href={`https://ra.co${event.eventUrl}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-500 hover:underline"
                        >
                          {event.eventName}
                        </a>
                      </td>
                      <td className="p-2">{new Date(event.date).toLocaleDateString()}</td>
                      <td className="p-2">{event.venue}</td>
                      <td className="p-2">{event.artists.join(', ')}</td>
                      <td className="p-2 text-right">{event.attendingCount}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
} 
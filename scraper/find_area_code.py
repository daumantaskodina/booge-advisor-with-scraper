import requests
import json
import time

URL = 'https://ra.co/graphql'
HEADERS = {
    'Content-Type': 'application/json',
    'Referer': 'https://ra.co/events/de/berlin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
}

# GraphQL query to get area information
area_query = {
    "operationName": "GET_AREA_FILTER",
    "variables": {},
    "query": "query GET_AREA_FILTER { filterItems { area { id title subTitle } } }"
}

# Try to get the area codes
try:
    response = requests.post(URL, headers=HEADERS, json=area_query)
    response.raise_for_status()
    data = response.json()
    
    if 'data' in data and 'filterItems' in data['data'] and 'area' in data['data']['filterItems']:
        areas = data['data']['filterItems']['area']
        print("Found area codes:")
        for area in areas:
            print(f"ID: {area['id']}, Title: {area['title']}, SubTitle: {area.get('subTitle', '')}")
            if "berlin" in area['title'].lower() or (area.get('subTitle') and "berlin" in area['subTitle'].lower()):
                print(f"BERLIN FOUND: Area code for Berlin is likely {area['id']}")
    else:
        print("Area data not found in the expected structure.")
        print("Response:", data)
        
except Exception as e:
    print(f"Error: {e}")
    print("Trying common area codes for Berlin...")

# If the above doesn't work, let's test some common area codes
test_area_codes = [13, 34, 73, 8, 3]  # Common European city codes based on RA patterns

for area_code in test_area_codes:
    print(f"Testing area code: {area_code}")
    
    # Create a simple query to test if this area code returns events for Berlin
    test_query = {
        "operationName": "GET_EVENT_LISTINGS",
        "variables": {
            "filters": {
                "areas": {"eq": area_code},
                "listingDate": {
                    "gte": "2025-05-19T00:00:00.000Z",
                    "lte": "2025-05-25T23:59:59.999Z"
                }
            },
            "pageSize": 1,
            "page": 1
        },
        "query": "query GET_EVENT_LISTINGS($filters: FilterInputDtoInput, $page: Int, $pageSize: Int) {eventListings(filters: $filters, pageSize: $pageSize, page: $page) {data {event {venue {name} __typename} __typename} __typename}}"
    }
    
    try:
        response = requests.post(URL, headers=HEADERS, json=test_query)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and 'eventListings' in data['data'] and 'data' in data['data']['eventListings'] and data['data']['eventListings']['data']:
            first_event = data['data']['eventListings']['data'][0]
            if 'event' in first_event and 'venue' in first_event['event'] and 'name' in first_event['event']['venue']:
                venue_name = first_event['event']['venue']['name']
                print(f"Found venue: {venue_name}")
                print(f"This area code ({area_code}) returns results. It might be Berlin if the venue looks correct.")
            else:
                print("No venue data found in the response.")
        else:
            print(f"No events found for area code {area_code}.")
            
    except Exception as e:
        print(f"Error testing area code {area_code}: {e}")
    
    # Be nice to the server
    time.sleep(1) 
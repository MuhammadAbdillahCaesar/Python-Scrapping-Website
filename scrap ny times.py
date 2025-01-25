import requests
import pandas as pd
from time import sleep

# Replace with your New York Times API key
API_KEY = 'k6P0Fziynqc3PUbf400OhE2WX1Z8mXLS'  # Replace this with your actual API key
max_articles = 500
keyword = "AI"
section = "Technology"
start_date = "20200101"  # Format: YYYYMMDD (January 1, 2020)
end_date = "20241101"    # Format: YYYYMMDD (November 1, 2024)
articles = []


# NYT Article Search API endpoint
url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

# Pagination parameters
page = 0  # Start from page 0
unique_titles = set()  # Set to track unique article titles

while len(articles) < max_articles:
    # Define the parameters for the API request
    params = {
        "q": keyword,
        "fq": f"section_name:(\"{section}\")",
        "begin_date": start_date,
        "end_date": end_date,
        "sort": "relevance",
        "page": page,
        "api-key": API_KEY
    }

    # Make the API request
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        # Check if there are articles in the response
        if 'response' in data and 'docs' in data['response']:
            docs = data['response']['docs']  # Initialize docs here
            if not docs:  # Break if no more articles are found
                print("No more articles found.")
                break
            
            for doc in docs:
                # Extract article details
                pub_date = doc.get('pub_date', 'N/A')
                title = doc.get('headline', {}).get('main', 'N/A')

                # Check for duplicate titles
                if title in unique_titles:
                    continue  # Skip if the title is already in the set
                unique_titles.add(title)  # Add title to the set

                summary = doc.get('abstract', 'N/A')
                author = doc.get('byline', {}).get('original', 'N/A')
                
                # Add the article to the list
                articles.append({
                    "Date": pub_date,
                    "Title": title,
                    "Summary": summary,
                    "Author": author
                })

                # Update progress
                progress = (len(articles) / max_articles) * 100
                print(f"Scraping Progress: {progress:.2f}% ({len(articles)}/{max_articles})", end='\r')

                # Stop if we've reached the target count
                if len(articles) >= max_articles:
                    break
        else:
            print("No articles returned in the response.")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")  # Print the HTTP error
        break  # Exit the loop on HTTP error
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")  # Print any other error
        break  # Exit the loop on request error

    # Increment the page to get the next set of results
    page += 1
    sleep(12)  # Pause to avoid hitting API rate limits

# Save the data to an Excel file
df = pd.DataFrame(articles)
df.to_excel('NYTimes_AI_Articles_API.xlsx', index=False)
print("\nData saved to NYTimes_AI_Articles_API.xlsx")

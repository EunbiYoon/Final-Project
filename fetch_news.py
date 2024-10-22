import requests

def fetch_news_api():
    ####### Settings ---> Change Variable ######
    search_keyword = 'apple stock'
    start_date = "2024-10-21"
    end_date = "2024-10-22" 
    sort_method = 'popularity'
    api_key = "fcf6368111ce48c3b234b0a479d1dca6"

    # url definition
    url = (
        "https://newsapi.org/v2/everything?"
        f"q={search_keyword}&"
        f"from={start_date}&"
        f"to={end_date}&"
        f"sortBy={sort_method}&"
        f"apiKey={api_key}"
    )

    try:
        # Make a request to the NewsAPI
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Print the total number of results
            total_results = data.get('totalResults', 0)
            print(f"Total results found: {total_results}")

            # Extract the articles
            articles = data.get('articles', [])
            # Check if articles were found
            if articles:
                for article in articles:
                    print(f"Title: {article.get('title')}")
                    print(f"Description: {article.get('description')}")
                    print(f"URL: {article.get('url')}\n")
            else:
                print("No articles found.")
        else:
            print(f"Failed to retrieve data: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_news_api()
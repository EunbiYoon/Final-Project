import requests
import json

def fetch_news_about_apple():
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
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Save the JSON data to a file
        with open('news_data.txt', 'w') as f:
            json.dump(data, f, indent=4)
        print("Data saved to 'news_data.txt'")
    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")

if __name__ == "__main__":
    fetch_news_about_apple()

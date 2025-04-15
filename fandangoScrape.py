from bs4 import BeautifulSoup as soup
import requests
import pandas as pd

# Fandango movies to scrape
urls = [
    "https://www.fandango.com/mickey-17-2025-238218/movie-overview", # Mickey 17
    "https://www.fandango.com/a-minecraft-movie-2025-216995/movie-overview", # A Minecraft movie
    "https://www.fandango.com/sinners-2025-237956/movie-overview", # Sinners
]

headers = {
    'User-agent':
    "Safari/537.36"
}

results_df = pd.DataFrame()

# Loop through each URL and extract movie details
for url in urls:
    response = requests.get(url, headers=headers)
    page_soup = soup(response.content, "html.parser")

    # Extract main movie details
    movies_data = []
    title = page_soup.find("h1").text.strip()
    year = page_soup.find("h1").text.strip()
    genres = page_soup.find("li", {"class": "movie-detail__grv-item dark__text"}).text.strip()
    rating = page_soup.find("aside", {"class": "movie-detail__additional-info"}).text.strip()
    synopsis = page_soup.find("p", {"id": "movie-detail-synopsis"}).text.strip()

    # Create csv file with extracted movie data
    movies_data.append([title, genres, rating, synopsis])
    temp_df = pd.DataFrame(movies_data, columns=["Title and Year", "Genre", "Additional Info", "Synopsis"])
    results_df = results_df.append(temp_df).reset_index(drop=True)

results_df.to_csv('results/fandango_movies.csv', index=False)

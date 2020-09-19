# [DEPRECATED]
I was told that Tripadvisor switched to a dynamic website so this scrapper became useless as it always scrapes the first page. Use it with caution. See if there's still some usefull pieces of code or feel free to contact me for whichever reason you desire: doubts, suggestions, etc. I do not plan, in the near future to maintain this project.

# Tripadvisor Restaurants Scraper

The idea of this project is to provide a tool that collects information from all the restaurants of a particular city. It currently gets the restaurant's:
`name, price range, rating, number of reviews, address, locality, and the url from which the data was extracted` and creates a CSV with the name "Restaurants_{city}_{date}.csv"
It was first intended to be used with Google Maps API but it's no longer free to query so scraping tripadvisor was the next best alternative.

## Run the program

- First of all you need to install [Python](https://www.python.org/downloads/release/python-368/) with a version equal or greater than 3.6

- Clone the repo
```
$ git clone https://github.com/augustobottelli/tripadvisor-restaurant-scraper.git
```

- Install the repository requirements.txt
```bash
$ pip3 install -r requirements.txt
```

- Run the program
```
$ python3 restaurants_scraper.py --city "Buenos Aires"
```
- If you wish to scrape just X pages instead of the whole catalog, you can include:
```
$ python3 restaurants_scraper.py --city "Buenos Aires" --max_pages X
```

It currently works for these cities:
- Buenos Aires
- Panama City
- Rio de Janeiro
- Sao Paulo
- Montevideo
- La Paz
- Santiago
- Asuncion

More cities can be added by including its city code and name from tripadvisor URL.

**It doesn't support multiple cities at once.**

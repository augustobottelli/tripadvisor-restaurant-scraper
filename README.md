# Tripadvisor Restaurants Scraper

The idea of this project is to provide a tool that collects information from all the restaurants of a particular city. It currently gets the restaurant's:
`name, price range, rating, number of reviews, address, locality, and the url from which the data was extracted.`
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
$ python3 restaurants_scraper.py --city 'Buenos Aires'
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

## Disclaimer
As mentioned before, the program is a web scraper and its correctness relies on Tripadvisor's HTML structure. If the page suffers changes, the program will break.
As of today **2019/01/07 the program still works**
import requests
import ast
import logging
import argparse
from pandas import DataFrame
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing.pool import ThreadPool
import re

logging.basicConfig(level=logging.INFO)

PAGE_OFFSET_INTERVAL = 30
BASE_URL = "https://www.tripadvisor.com"
N_THREADS = 8  # Depends on personal computer threads
DATE = datetime.now().strftime("%Y-%m-%d")


def get_html_and_parse(url):
    req = requests.get(url)
    url_html = BeautifulSoup(req.text, "html.parser")
    return url_html


def _get_last_page_offset(url_html):
    """Obtain last page offset.

    Required to stop iterating over pages.

    Parameters
    ----------
    url_html : BeautifulSoup object

    Returns
    -------
    int

    """
    page_numbers = url_html.findAll("div", attrs={"class": "pageNumbers"})[0]
    last_page_offset = page_numbers.findAll("a")[-1].get("data-offset")
    return int(last_page_offset)


def _restaurant_info(restaurant_data, email):
    restaurant_dict = {
        "name": restaurant_data.get("name"),
        "priceRange": restaurant_data.get("priceRange"),
        "rating": restaurant_data.get("aggregateRating").get("ratingValue"),
        "reviewCount": restaurant_data.get("aggregateRating").get("reviewCount"),
        "address": restaurant_data.get("address").get("streetAddress"),
        "locality": restaurant_data.get("address").get("addressLocality"),
        "url": BASE_URL + restaurant_data.get("url"),
        'email': email
    }
    return restaurant_dict


def city_filter(city):
    city_filter = {
        "Panama City": ("g294480", "Panama_City_Panama_Province"),
        "Buenos Aires": ("g312741", "Buenos_Aires_Capital_Federal_District"),
        "Rio de Janeiro": ("g303506", "Rio_de_Janeiro_State_of_Rio_de_Janeiro"),
        "Montevideo": ("g294323", "Montevideo_Montevideo_Department"),
        "Santiago": ("g294305", "Santiago_Santiago_Metropolitan_Region"),
        "Asuncion": ("g294080", "Asuncion"),
        "Sao Paulo": ("g303631", "Sao_Paulo_State_of_Sao_Paulo"),
        "La Paz": ("g294072", "La_Paz_La_Paz_Department"),
    }
    city_information = city_filter.get(city)
    if city_information is None:
        logging.error(f"Available cities: {list(city_filter.keys())}")
    else:
        return city_information


def get_restaurants_info(restaurants_list, url_html, thread_pool):
    """Find and save restaurants information into a list.

    The href that ends with #REVIEWS was chosen to avoid duplicates.

    Parameters
    ----------
    restaurants_list : list
        list which will contain all of the restaurants information
    url_html : BeautifulSoup object
        html of the page scraped
    thread_pool : ThreadPool object
        object that will parallelize requests in order to speed up the process.

    """
    def get_restaurant_info(restaurant_tag):
        restaurant_url = BASE_URL + restaurant_tag.get("href")
        restaurant_html = get_html_and_parse(restaurant_url)
        restaurant_data = restaurant_html.findAll("script")[1].contents[0]
        restaurant_data = ast.literal_eval(restaurant_data)
        try:
            mailA = restaurant_html.findAll('a', href=re.compile("mailto"))
            em = mailA[0]['href'].split('?')[0][len("mailto") + 1:]
        except:
            em = ''
        restaurant_information = _restaurant_info(restaurant_data, em)
        if restaurant_information:
            restaurants_list.append(restaurant_information)
        else:
            logging.warning("Missing restaurant information")

    restaurants_component = url_html.findAll(attrs={"id": "component_2"})
    restaurants_tags = filter(
        lambda x: x.get("href").startswith("/Restaurant_Review")
        and x.get("href").endswith("#REVIEWS"),
        restaurants_component[0].findAll("a"),
    )
    thread_pool.map(lambda x: get_restaurant_info(x), restaurants_tags)


def _set_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", type=str, required=True, help="Need to specify a city")
    parser.add_argument("--max_pages", type=int)
    args, unknown = parser.parse_known_args()
    if unknown:
        logging.warning(f"Unknown parameter {unknown}")
    if not args.city:
        logging.error("Need to provide a city")
    else:
        return args


def _make_csv(restaurants_lists, city, date):
    columns = list(restaurants_lists[0].keys())
    df = DataFrame(restaurants_lists, columns=columns)
    csv_name = f"Restaurants_{city}_{date}.csv"
    logging.info(f"Saving CSV as {csv_name}")
    df.to_csv(csv_name, index=False)


if __name__ == "__main__":
    args = _set_cli()
    restaurants_data = []
    city_code, city_name = city_filter(args.city)
    logging.info(f"Scraping Tripadvisor restaurants data from {args.city}")

    page_offset = 0
    full_url = BASE_URL + f"/Restaurants-{city_code}-oa{page_offset}-{city_name}"
    first_page = get_html_and_parse(full_url)
    if not args.max_pages:
        last_page_offset = _get_last_page_offset(first_page)
    else:
        last_page_offset = (args.max_pages - 1) * PAGE_OFFSET_INTERVAL
    last_page = (last_page_offset / PAGE_OFFSET_INTERVAL) + 1

    logging.info(f"Scraping page 1 of {int(last_page)}")
    thread_pool = ThreadPool(N_THREADS)
    first_page_info = get_restaurants_info(restaurants_data, first_page, thread_pool)
    while page_offset < last_page_offset:
        page_offset += PAGE_OFFSET_INTERVAL
        page_number = (page_offset / PAGE_OFFSET_INTERVAL) + 1
        page_html = get_html_and_parse(full_url)
        logging.info(f"Scraping page {int(page_number)} of {int(last_page)}")
        restaurants_information = get_restaurants_info(
            restaurants_data, page_html, thread_pool
        )
    _make_csv(restaurants_data, args.city, DATE)

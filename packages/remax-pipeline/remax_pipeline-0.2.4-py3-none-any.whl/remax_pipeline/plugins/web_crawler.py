import itertools
import multiprocessing
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import date

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from ..services import generate_listing_primary_key, generate_uuid_from_string
from ..services.fileio_service import write_to_json_local
from ..services.selenium_service import HTMLStackParser, get_driver
from ..utils.logging import logger


class RemaxExecutor:
    def __init__(self, multithreaded: bool = True, max_workers: int = multiprocessing.cpu_count()):
        self.multithreaded = multithreaded
        self.max_workers = max_workers

    @staticmethod
    def _create_chunks(n, m):

        chunks = []
        chunk_size = n // m
        remainder = n % m

        for i in range(0, m):
            start = i * chunk_size
            end = start + chunk_size
            if i == m - 1:  #
                end += remainder
            chunks.append(list(range(start + 1, end + 1)))

        return chunks

    @staticmethod
    def _create_bins(n, m):
        return [list(range(i, min(i + m, n + 1))) for i in range(1, n + 1, m)]

    def get_workload(self, m: int = 12, distribution_type: str = "bin", n=None):

        if distribution_type not in ["bin", "chunk"]:
            raise Exception("Distribution type should be either 'bin' or 'chunk'")

        if n is None:
            total_pages = self.get_total_pages()
        else:
            total_pages = n

        action = {
            "bin": RemaxExecutor._create_bins,
            "chunk": RemaxExecutor._create_chunks,
        }

        return action[distribution_type](total_pages, m)

    def get_total_pages(self):

        self.driver = get_driver()

        url = "https://www.remax.ca/on/toronto-real-estate?pageNumber=1"

        self.driver.get(url)

        total_pages = int(
            self.driver.find_element(By.CLASS_NAME, "page-control_buttonRowContainer__wfw6_")
            .find_elements(By.TAG_NAME, "a")[-1]
            .get_attribute("href")
            .split("pageNumber=")[-1]
        )

        self.driver.close()

        return total_pages

    def task(self, page_number):
        if self.multithreaded:
            logger.task(f"Thread - page: {page_number}")
        else:
            logger.task(f"Sequential - page: {page_number}")

        listing = WebCrawler(page_number).crawl()

        return listing

    def get_multipage_listing(self, pages, output=False, filename=None):

        if self.multithreaded:
            logger.task("Running with threads...")
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                result = executor.map(self.task, pages)
            result = list(itertools.chain.from_iterable([i for i in result]))

        else:
            logger.task("Running sequentially...")
            result = list(itertools.chain.from_iterable([self.task(i) for i in pages]))

        if output:
            write_to_json_local(result, filename)

        return result


class WebCrawler:
    """Bot that scrapes listings from a single page"""

    def __init__(self, page_number=1):

        logger.info("Creating page instance")
        self.driver = get_driver()
        self.listing_link = f"https://www.remax.ca/on/toronto-real-estate?pageNumber={page_number}"

    def crawl(self, location="Toronto"):
        self.driver.get(self.listing_link)

        listings = [
            element.get_attribute("href")
            for element in self.driver.find_elements(By.CLASS_NAME, "listing-card_listingCard__G6M8g")
        ]
        logger.info(listings)
        result = [self.get_listing_data(i) for i in listings]

        logger.info("Closing page instance")
        self.driver.close()

        return result

    def _get_listing_description(self):

        try:
            return self.driver.find_element(By.XPATH, '//*[@id="description"]/summary/p').text
        except NoSuchElementException:
            return None

    def get_listing_data(self, url) -> dict:

        self.driver.get(url)
        try:
            return {
                **self._get_listing_location(),
                **self._get_listing_price_details(),
                "description": self._get_listing_description(),
                "listing_date": date.today(),
            }
        except Exception as e:
            logger.warning(f"{e}, {url}")
            return {}

    def _get_listing_location(self):

        parsed_element = HTMLStackParser.parse_web_element(
            self.driver.find_element(By.CLASS_NAME, "listing-summary_addressAgentWrapper__0H3ys")
        )

        lat = float(self.driver.find_element(By.XPATH, "/html/head/meta[10]").get_attribute("content"))

        lon = float(self.driver.find_element(By.XPATH, "/html/head/meta[11]").get_attribute("content"))

        return {**self._parse_address(parsed_element), **{"lat": lat, "lon": lon}}

    def _clean_web_element(self, parsed_element):
        return [" ".join(i.split()) for i in parsed_element]

    def _parse_address(self, parsed_element: list):

        street_name = parsed_element[0]
        city_details = parsed_element[1].split(", ")
        full_address = ", ".join(parsed_element)

        return {
            "id": generate_listing_primary_key(full_address),
            "address_id": generate_uuid_from_string(full_address),
            "full_address": full_address,
            "street_name": street_name,
            "city": city_details[0],
            "province": city_details[1],
            "postal_code": city_details[2],
        }

    def _get_listing_price_details(self) -> dict:

        parsed_element = self._clean_web_element(
            HTMLStackParser.parse_web_element(
                self.driver.find_element(By.CLASS_NAME, "listing-summary_priceDetailsWrapper__z_9hg")
            )
        )

        assert parsed_element[0][0] == "$"
        price = float(re.sub("[^A-Za-z0-9]+", "", parsed_element[0]))

        assert "bed" in parsed_element
        bed_index = parsed_element.index("bed")
        bed = parsed_element[bed_index - 1]
        bed = int(bed) if bed.isdigit() else None

        assert "bath" in parsed_element
        bath_index = parsed_element.index("bath")
        bath = parsed_element[bath_index - 1]
        bath = int(bath) if bath.isdigit() else None

        property_type = parsed_element[-1]

        listing = {
            "home_price": price,
            "bed": bed,
            "bath": bath,
            "property_type": property_type,
        }

        return listing

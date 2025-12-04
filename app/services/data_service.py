import logging

from app.databases.db import get_postgresql_db_contextmanager
from app.databases.repository import CountryRepository
from app.utils.html_manager import HtmlManager
from app.parsers.parser_factory import ParserFactory


class DataService:
    def __init__(self, html_manager: HtmlManager):
        self.html_manager = html_manager

    async def get_data(self, source_url: str):
        file_name = "wiki" if "wikipedia" in source_url else "stat-files"

        if self.html_manager.find_html_file(file_name):
            soup = self.html_manager.read_html(file_name)
        else:
            soup = await self.html_manager.fetch_html(source_url)
            self.html_manager.write_html(soup, file_name)

        parser = ParserFactory.create(source_url, soup)
        countries = parser.retrieve_countries()

        async with get_postgresql_db_contextmanager() as session:
            repo = CountryRepository(session)
            await repo.add_many(countries)
        print("Inserting data successfully finished")

    @staticmethod
    async def print_data():
        async with get_postgresql_db_contextmanager() as session:
            repo = CountryRepository(session)

            if not await repo.verify_db():
                logging.warning("No data to print. Please use `docker-compose up get_data` first")
                return

            countries = await repo.get_countries()

            for country in countries:
                logging.info(f"Region: {country['region']}")
                logging.info(f"Total population: {country['total_population']}")
                logging.info(
                    f"Largest country in the region (population): "
                    f"{country['largest_country']}"
                )
                logging.info(f"Largest population in there: {country['largest_population']}")
                logging.info(
                    f"Smallest country in the region (population): "
                    f"{country['smallest_country']}"
                )
                logging.info(f"Smallest population in there: {country['smallest_population']}\n")

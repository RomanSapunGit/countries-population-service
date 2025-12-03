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
                print("No data to print. Please use `docker-compose up get_data` first")

            countries = await repo.get_countries()
            for country in countries:
                print(f"Region: {country['region']}")
                print(f"Total population: {country['total_population']}")
                print(f"Largest country in the region (population): {country['largest_country']}")
                print(f"Largest population in there: {country['largest_population']}")
                print(f"Smallest country in the region (population): {country['smallest_country']}")
                print(f"Smallest population in there: {country['smallest_population']}\n")

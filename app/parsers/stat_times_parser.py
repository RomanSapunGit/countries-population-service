from bs4 import Tag

from app.databases.models import CountryModel
from app.parsers.base_parser import BaseParser


class StatisticsTimesParser(BaseParser):
    def retrieve_countries(self):
        country_rows = self._soup.select_one("#table_id").find_all("tr")
        return [
            self._parse_country(country_rows[i])
            for i in range(2, len(country_rows) - 1)
        ]

    def _parse_country(self, country_tag: Tag):
        country_tag = country_tag.find_all("td")
        population = "".join(filter(str.isdigit, country_tag[3].text))
        return CountryModel(
            name=country_tag[0].find("a").text.strip(),
            region=country_tag[-1].text.strip(),
            population=int(population)
        )

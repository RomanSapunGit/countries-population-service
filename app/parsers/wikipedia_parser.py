from bs4 import Tag

from app.databases.models import CountryModel
from app.parsers.base_parser import BaseParser


class WikipediaParser(BaseParser):
    def _parse_country(self, country_tag: Tag) -> CountryModel:
        td_list = country_tag.find_all("td")
        population = "".join(filter(str.isdigit, td_list[2].text))

        return CountryModel(
            name=country_tag.find("a").text.strip(),
            region=td_list[-1].text.strip(),
            population=int(population)
        )

    @staticmethod
    def find_not_available_data(tag: Tag):
        td_tag = tag.find_all("td")
        return "N/A" == td_tag[2].text.strip()

    def retrieve_countries(self) -> list[CountryModel]:
        country_rows = self._soup.find(class_="wikitable").find_all("tr")

        return [
            self._parse_country(country_rows[i])
            for i in range(2, len(country_rows))
            if not self.find_not_available_data(country_rows[i])
        ]

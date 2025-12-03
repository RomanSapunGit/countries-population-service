from abc import abstractmethod, ABC
from bs4 import BeautifulSoup, Tag

from app.databases.models import CountryModel


class BaseParser(ABC):
    def __init__(self, soup: BeautifulSoup):
        self._soup = soup

    @abstractmethod
    def _parse_country(self, country_tag: Tag):
        pass

    @abstractmethod
    def retrieve_countries(self) -> list[CountryModel]:
        pass

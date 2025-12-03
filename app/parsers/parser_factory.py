from bs4 import BeautifulSoup

from app.parsers.base_parser import BaseParser
from app.parsers.stat_times_parser import StatisticsTimesParser
from app.parsers.wikipedia_parser import WikipediaParser


class ParserFactory:
    @staticmethod
    def create(source_url: str, soup: BeautifulSoup) -> BaseParser:
        if "wikipedia" in source_url.lower():
            return WikipediaParser(soup)
        elif "statisticstimes" in source_url.lower():
            return StatisticsTimesParser(soup)
        else:
            raise ValueError(f"No parser implemented for source: {source_url}")

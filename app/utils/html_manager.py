from os import walk

from bs4 import BeautifulSoup
from httpx import AsyncClient

from app.config.config import AppSettings


class HtmlManager:
    def __init__(self, base_dir: str, settings: AppSettings):
        self.base_dir = base_dir
        self.headers = {
            "User-Agent": settings.AGENT
        }

    def find_html_file(self, file_name: str) -> bool:
        for root, dirs, files in walk(self.base_dir):
            if file_name in files:
                return True
        return False

    async def fetch_html(self, url: str) -> BeautifulSoup:
        async with AsyncClient(timeout=20.0) as client:
            resp = await client.get(url, headers=self.headers)
            return BeautifulSoup(resp.content, "html.parser")

    def read_html(self, file_name: str) -> BeautifulSoup:
        with open(f"{self.base_dir}/{file_name}.html", "r", encoding="utf-8") as file:
            content = file.read()
        return BeautifulSoup(content, "html.parser")

    def write_html(self, soup: BeautifulSoup, file_name: str):
        with open(f"{self.base_dir}/{file_name}.html", "w", encoding="utf-8") as file:
            file.write(soup.prettify())

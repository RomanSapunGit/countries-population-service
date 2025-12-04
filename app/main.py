import asyncio
import logging
from sys import argv

from app.config.config import settings
from app.services.data_service import DataService
from app.utils.html_manager import HtmlManager

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

async def main():
    html_manager = HtmlManager(settings.BASE_DIR, settings)
    service = DataService(html_manager)

    if len(argv) < 2:
        logging.error("Usage: python main.py [get_data|print_data]")
        return

    command = argv[1].lower()

    if command == "get_data":
        logging.info("Fetching and storing data...")
        await service.get_data(settings.SOURCE_URL)
    elif command == "print_data":
        logging.info("Printing aggregated data...")
        await service.print_data()
    else:
        logging.error(f"Unknown command: {command}")

if __name__ == "__main__":
    asyncio.run(main())

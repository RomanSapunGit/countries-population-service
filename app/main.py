import asyncio
from sys import argv

from app.config.config import settings
from app.utils.data_service import DataService
from app.utils.html_manager import HtmlManager


async def main():
    html_manager = HtmlManager(settings.BASE_DIR, settings)
    service = DataService(html_manager)
    if len(argv) < 2:
        print("Usage: python main.py [get_data|print_data]")
        return

    command = argv[1].lower()

    if command == "get_data":
        await service.get_data(settings.SOURCE_URL)
    elif command == "print_data":
        await service.print_data()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    asyncio.run(main())

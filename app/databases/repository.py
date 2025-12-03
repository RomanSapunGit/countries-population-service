from typing import Any, Coroutine, Sequence

from sqlalchemy import select, func, distinct, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.models import CountryModel


class CountryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_many(self, countries: list[CountryModel]):
        self._session.add_all(countries)
        await self._session.commit()

    async def verify_db(self):
        stmt = select(func.count(CountryModel.id))
        result = await self._session.execute(stmt)
        countries_count = result.scalar()

        if countries_count == 0:
            return False

        return True

    async def get_countries(self) -> Sequence[RowMapping]:
        region_stats_subq = (
            select(
                CountryModel.region,
                func.sum(CountryModel.population).label("total_population")
            )
            .group_by(CountryModel.region).subquery())

        largest_subq = (
            select(
                CountryModel.region,
                CountryModel.name.label("largest_country"),
                CountryModel.population.label("largest_population")
            )
            .distinct(CountryModel.region)
            .order_by(CountryModel.region, CountryModel.population.desc())
        ).subquery()

        smallest_subq = (
            select(
                CountryModel.region,
                CountryModel.name.label("smallest_country"),
                CountryModel.population.label("smallest_population")
            )
            .distinct(CountryModel.region)
            .order_by(CountryModel.region, CountryModel.population)
        ).subquery()

        result_stmt = (select(
            region_stats_subq.c.region,
            region_stats_subq.c.total_population,
            largest_subq.c.largest_country,
            largest_subq.c.largest_population,
            smallest_subq.c.smallest_country,
            smallest_subq.c.smallest_population
        )
            .join(largest_subq, largest_subq.c.region == region_stats_subq.c.region)
            .join(smallest_subq, smallest_subq.c.region == region_stats_subq.c.region)
            .order_by(region_stats_subq.c.region)
        )

        countries_result = await self._session.execute(result_stmt)
        return countries_result.mappings().all()

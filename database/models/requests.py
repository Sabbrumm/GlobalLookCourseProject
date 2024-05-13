from sqlalchemy import select, update, delete
from sqlalchemy.sql.elements import BinaryExpression

from database import async_session_factory
from database.models.tables import *


class PassportsTable(object):
	@staticmethod
	async def create_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				passports: Passports = Passports(id=id_)
				session.add(passports)
				await session.commit()
				return True
		except Exception as e:
			print(e)
			return False

	@staticmethod
	async def get_where(exp: BinaryExpression) -> Passports | None:
		try:
			async with async_session_factory() as session:
				expression = select(Passports).where(exp)
				query = await session.execute(expression)
				passports: Passports = query.scalar()
				await session.close()
				return passports
		except Exception as e:
			print(e)
			return None

	@staticmethod
	async def get_by_id(id_: int) -> Passports | None:
		try:
			async with async_session_factory() as session:
				passports: Passports = await session.get(Passports, id_)
				await session.close()
				return passports
		except Exception as e:
			print(e)

			return None

	@staticmethod
	async def update_by_id(id_: int, **kwargs) -> bool:
		try:
			async with async_session_factory() as session:
				expression = update(Passports).where(Passports.id == id_).values(kwargs)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_where(exp: BinaryExpression) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(Passports).where(exp)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(Passports).where(Passports.id == id_)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False


class PersonsTable(object):
	@staticmethod
	async def create_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				persons: Persons = Persons(id=id_)
				session.add(persons)
				await session.commit()
				return True
		except Exception as e:
			print(e)
			return False

	@staticmethod
	async def get_where(exp: BinaryExpression) -> Persons | None:
		try:
			async with async_session_factory() as session:
				expression = select(Persons).where(exp)
				query = await session.execute(expression)
				persons: Persons = query.scalar()
				await session.close()
				return persons
		except Exception as e:
			print(e)
			return None

	@staticmethod
	async def get_by_id(id_: int) -> Persons | None:
		try:
			async with async_session_factory() as session:
				persons: Persons = await session.get(Persons, id_)
				await session.close()
				return persons
		except Exception as e:
			print(e)

			return None

	@staticmethod
	async def update_by_id(id_: int, **kwargs) -> bool:
		try:
			async with async_session_factory() as session:
				expression = update(Persons).where(Persons.id == id_).values(kwargs)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_where(exp: BinaryExpression) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(Persons).where(exp)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(Persons).where(Persons.id == id_)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False


class ReleasesTable(object):
	@staticmethod
	async def create_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				releases: Releases = Releases(id=id_)
				session.add(releases)
				await session.commit()
				return True
		except Exception as e:
			print(e)
			return False

	@staticmethod
	async def get_where(exp: BinaryExpression) -> Releases | None:
		try:
			async with async_session_factory() as session:
				expression = select(Releases).where(exp)
				query = await session.execute(expression)
				releases: Releases = query.scalar()
				await session.close()
				return releases
		except Exception as e:
			print(e)
			return None

	@staticmethod
	async def get_by_id(id_: int) -> Releases | None:
		try:
			async with async_session_factory() as session:
				releases: Releases = await session.get(Releases, id_)
				await session.close()
				return releases
		except Exception as e:
			print(e)

			return None

	@staticmethod
	async def update_by_id(id_: int, **kwargs) -> bool:
		try:
			async with async_session_factory() as session:
				expression = update(Releases).where(Releases.id == id_).values(kwargs)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_where(exp: BinaryExpression) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(Releases).where(exp)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(Releases).where(Releases.id == id_)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False


class PlatformsTable(object):
	@staticmethod
	async def create_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				platforms: Platforms = Platforms(id=id_)
				session.add(platforms)
				await session.commit()
				return True
		except Exception as e:
			print(e)
			return False

	@staticmethod
	async def get_where(exp: BinaryExpression) -> Platforms | None:
		try:
			async with async_session_factory() as session:
				expression = select(Platforms).where(exp)
				query = await session.execute(expression)
				platforms: Platforms = query.scalar()
				await session.close()
				return platforms
		except Exception as e:
			print(e)
			return None

	@staticmethod
	async def get_by_id(id_: int) -> Platforms | None:
		try:
			async with async_session_factory() as session:
				platforms: Platforms = await session.get(Platforms, id_)
				await session.close()
				return platforms
		except Exception as e:
			print(e)

			return None

	@staticmethod
	async def update_by_id(id_: int, **kwargs) -> bool:
		try:
			async with async_session_factory() as session:
				expression = update(Platforms).where(Platforms.id == id_).values(kwargs)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_where(exp: BinaryExpression) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(Platforms).where(exp)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(Platforms).where(Platforms.id == id_)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False


class RegionsTable(object):
	@staticmethod
	async def create_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				regions: Regions = Regions(id=id_)
				session.add(regions)
				await session.commit()
				return True
		except Exception as e:
			print(e)
			return False

	@staticmethod
	async def get_where(exp: BinaryExpression) -> Regions | None:
		try:
			async with async_session_factory() as session:
				expression = select(Regions).where(exp)
				query = await session.execute(expression)
				regions: Regions = query.scalar()
				await session.close()
				return regions
		except Exception as e:
			print(e)
			return None

	@staticmethod
	async def get_by_id(id_: int) -> Regions | None:
		try:
			async with async_session_factory() as session:
				regions: Regions = await session.get(Regions, id_)
				await session.close()
				return regions
		except Exception as e:
			print(e)

			return None

	@staticmethod
	async def update_by_id(id_: int, **kwargs) -> bool:
		try:
			async with async_session_factory() as session:
				expression = update(Regions).where(Regions.id == id_).values(kwargs)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_where(exp: BinaryExpression) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(Regions).where(exp)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(Regions).where(Regions.id == id_)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False


class TracksTable(object):
	@staticmethod
	async def create_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				tracks: Tracks = Tracks(id=id_)
				session.add(tracks)
				await session.commit()
				return True
		except Exception as e:
			print(e)
			return False

	@staticmethod
	async def get_where(exp: BinaryExpression) -> Tracks | None:
		try:
			async with async_session_factory() as session:
				expression = select(Tracks).where(exp)
				query = await session.execute(expression)
				tracks: Tracks = query.scalar()
				await session.close()
				return tracks
		except Exception as e:
			print(e)
			return None

	@staticmethod
	async def get_by_id(id_: int) -> Tracks | None:
		try:
			async with async_session_factory() as session:
				tracks: Tracks = await session.get(Tracks, id_)
				await session.close()
				return tracks
		except Exception as e:
			print(e)

			return None

	@staticmethod
	async def update_by_id(id_: int, **kwargs) -> bool:
		try:
			async with async_session_factory() as session:
				expression = update(Tracks).where(Tracks.id == id_).values(kwargs)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_where(exp: BinaryExpression) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(Tracks).where(exp)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(Tracks).where(Tracks.id == id_)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False


class MusicianCardsTable(object):
	@staticmethod
	async def create_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				musician_cards: MusicianCards = MusicianCards(id=id_)
				session.add(musician_cards)
				await session.commit()
				return True
		except Exception as e:
			print(e)
			return False

	@staticmethod
	async def get_where(exp: BinaryExpression) -> MusicianCards | None:
		try:
			async with async_session_factory() as session:
				expression = select(MusicianCards).where(exp)
				query = await session.execute(expression)
				musician_cards: MusicianCards = query.scalar()
				await session.close()
				return musician_cards
		except Exception as e:
			print(e)
			return None

	@staticmethod
	async def get_by_id(id_: int) -> MusicianCards | None:
		try:
			async with async_session_factory() as session:
				musician_cards: MusicianCards = await session.get(MusicianCards, id_)
				await session.close()
				return musician_cards
		except Exception as e:
			print(e)

			return None

	@staticmethod
	async def update_by_id(id_: int, **kwargs) -> bool:
		try:
			async with async_session_factory() as session:
				expression = update(MusicianCards).where(MusicianCards.id == id_).values(kwargs)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_where(exp: BinaryExpression) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(MusicianCards).where(exp)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(MusicianCards).where(MusicianCards.id == id_)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False


class ReleasesRolesTable(object):
	@staticmethod
	async def create_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				releases_roles: ReleasesRoles = ReleasesRoles(id=id_)
				session.add(releases_roles)
				await session.commit()
				return True
		except Exception as e:
			print(e)
			return False

	@staticmethod
	async def get_where(exp: BinaryExpression) -> ReleasesRoles | None:
		try:
			async with async_session_factory() as session:
				expression = select(ReleasesRoles).where(exp)
				query = await session.execute(expression)
				releases_roles: ReleasesRoles = query.scalar()
				await session.close()
				return releases_roles
		except Exception as e:
			print(e)
			return None

	@staticmethod
	async def get_by_id(id_: int) -> ReleasesRoles | None:
		try:
			async with async_session_factory() as session:
				releases_roles: ReleasesRoles = await session.get(ReleasesRoles, id_)
				await session.close()
				return releases_roles
		except Exception as e:
			print(e)

			return None

	@staticmethod
	async def update_by_id(id_: int, **kwargs) -> bool:
		try:
			async with async_session_factory() as session:
				expression = update(ReleasesRoles).where(ReleasesRoles.id == id_).values(kwargs)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_where(exp: BinaryExpression) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(ReleasesRoles).where(exp)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(ReleasesRoles).where(ReleasesRoles.id == id_)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False


class TracksRolesTable(object):
	@staticmethod
	async def create_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				tracks_roles: TracksRoles = TracksRoles(id=id_)
				session.add(tracks_roles)
				await session.commit()
				return True
		except Exception as e:
			print(e)
			return False

	@staticmethod
	async def get_where(exp: BinaryExpression) -> TracksRoles | None:
		try:
			async with async_session_factory() as session:
				expression = select(TracksRoles).where(exp)
				query = await session.execute(expression)
				tracks_roles: TracksRoles = query.scalar()
				await session.close()
				return tracks_roles
		except Exception as e:
			print(e)
			return None

	@staticmethod
	async def get_by_id(id_: int) -> TracksRoles | None:
		try:
			async with async_session_factory() as session:
				tracks_roles: TracksRoles = await session.get(TracksRoles, id_)
				await session.close()
				return tracks_roles
		except Exception as e:
			print(e)

			return None

	@staticmethod
	async def update_by_id(id_: int, **kwargs) -> bool:
		try:
			async with async_session_factory() as session:
				expression = update(TracksRoles).where(TracksRoles.id == id_).values(kwargs)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_where(exp: BinaryExpression) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(TracksRoles).where(exp)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(TracksRoles).where(TracksRoles.id == id_)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False


class ArtistsTable(object):
	@staticmethod
	async def create_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				artists: Artists = Artists(id=id_)
				session.add(artists)
				await session.commit()
				return True
		except Exception as e:
			print(e)
			return False

	@staticmethod
	async def get_where(exp: BinaryExpression) -> Artists | None:
		try:
			async with async_session_factory() as session:
				expression = select(Artists).where(exp)
				query = await session.execute(expression)
				artists: Artists = query.scalar()
				await session.close()
				return artists
		except Exception as e:
			print(e)
			return None

	@staticmethod
	async def get_by_id(id_: int) -> Artists | None:
		try:
			async with async_session_factory() as session:
				artists: Artists = await session.get(Artists, id_)
				await session.close()
				return artists
		except Exception as e:
			print(e)

			return None

	@staticmethod
	async def update_by_id(id_: int, **kwargs) -> bool:
		try:
			async with async_session_factory() as session:
				expression = update(Artists).where(Artists.id == id_).values(kwargs)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_where(exp: BinaryExpression) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(Artists).where(exp)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False

	@staticmethod
	async def del_by_id(id_: int) -> bool:
		try:
			async with async_session_factory() as session:
				expression = delete(Artists).where(Artists.id == id_)
				await session.execute(expression)
				await session.commit()
				await session.close()
				return True
		except Exception as e:
			print(e)

			return False



from Database import Db
import asyncio
from dataclasses import dataclass
from aiodesa.utils.tables import foreign_key, ForeignKey, unique_key, UniqueKey, primary_key, PrimaryKey


async def main():
	@dataclass
	@foreign_key(ForeignKey("username", "anothertable"))
	@primary_key(PrimaryKey("username"))
	@unique_key(UniqueKey("username"))
	class UserEcon:
		username: str
		credits: None | int = None
		points: int | None = None
		table_name: str = "user_economy"


	async with Db("database.sqlite3") as db:
		db.build_records(UserEcon)
		await db.read_table_schemas(UserEcon)
		record = db.insert_into(UserEcon.table_name, update=True)
		await record('sockheadrps', credits=100)

asyncio.run(main())
# Asyncio Dead Easy Sql API

## AIODesa is for simple data access and definition for your python projects

### AIODesa simplifies async SQLite database management for your projects. It provides a convenient wrapper around Asiosqlite, allowing easy definition of table and record schemas using Python's dataclasses. Define SQL tables and records effortlessly with AIODesa using a single data class, a tuple of data classes, or a .py file with dataclasses.

AIODesa aims to make defining SQL tables and records easy by utilizing dataclasses to define schemas of tables and records. Table and record schemas can be defined with:
1. a single data class
2. a tuple of data classes
3. a .py file with dataclasses.
<br>

# Usage

__Install via pip__
```
pip install aiodesa
```

Import db from the package and run with asyncio

__main.py__

```
from aiodesa.Database import Db
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
```

Tables are automatically generated    
![sql file](https://github.com/sockheadrps/AIODesa/blob/main/sql.png?raw=true)

<br>

# Development:

Ensure poetry is installed:

```
pip install poetry
```

Install project using poetry

```
poetry add git+https://github.com/sockheadrps/AIODesa.git
poetry install
```

create a python file for using AIODesa and activate poetry virtual env to run it

```
poetry shell
poetry run python main.py
```

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiodesa',
 'aiodesa.utils',
 'aiodesa.utils.records',
 'aiodesa.utils.tables',
 'aiodesa.utils.types']

package_data = \
{'': ['*']}

install_requires = \
['aiosqlite>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'aiodesa',
    'version': '0.1.8',
    'description': '',
    'long_description': '# Asyncio Dead Easy Sql API\n\n## AIODesa is for simple data access and definition for your python projects\n\n### AIODesa simplifies async SQLite database management for your projects. It provides a convenient wrapper around Asiosqlite, allowing easy definition of table and record schemas using Python\'s dataclasses. Define SQL tables and records effortlessly with AIODesa using a single data class, a tuple of data classes, or a .py file with dataclasses.\n\nAIODesa aims to make defining SQL tables and records easy by utilizing dataclasses to define schemas of tables and records. Table and record schemas can be defined with:\n1. a single data class\n2. a tuple of data classes\n3. a .py file with dataclasses.\n<br>\n\n# Usage\n\n__Install via pip__\n```\npip install aiodesa\n```\n\nImport db from the package and run with asyncio\n\n__main.py__\n\n```\nfrom aiodesa.Database import Db\nimport asyncio\nfrom dataclasses import dataclass\nfrom aiodesa.utils.tables import foreign_key, ForeignKey, unique_key, UniqueKey, primary_key, PrimaryKey\n\n\nasync def main():\n\t@dataclass\n\t@foreign_key(ForeignKey("username", "anothertable"))\n\t@primary_key(PrimaryKey("username"))\n\t@unique_key(UniqueKey("username"))\n\tclass UserEcon:\n\t\tusername: str\n\t\tcredits: None | int = None\n\t\tpoints: int | None = None\n\t\ttable_name: str = "user_economy"\n\n\n\tasync with Db("database.sqlite3") as db:\n\t\tdb.build_records(UserEcon)\n\t\tawait db.read_table_schemas(UserEcon)\n\t\trecord = db.insert_into(UserEcon.table_name, update=True)\n\t\tawait record(\'sockheadrps\', credits=100)\n\nasyncio.run(main())\n```\n\nTables are automatically generated    \n![sql file](https://github.com/sockheadrps/AIODesa/blob/main/sql.png?raw=true)\n\n<br>\n\n# Development:\n\nEnsure poetry is installed:\n\n```\npip install poetry\n```\n\nInstall project using poetry\n\n```\npoetry add git+https://github.com/sockheadrps/AIODesa.git\npoetry install\n```\n\ncreate a python file for using AIODesa and activate poetry virtual env to run it\n\n```\npoetry shell\npoetry run python main.py\n```\n',
    'author': 'sockheadrps',
    'author_email': 'r.p.skiles@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

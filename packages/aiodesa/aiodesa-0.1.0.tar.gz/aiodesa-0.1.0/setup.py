# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiodesa', 'aiodesa.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiosqlite>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'aiodesa',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Asyncio Dead Easy Sql API\n\n## AIODesa is for simple data access and definition for your python projects\n\n \n### AIODesa simplifies async SQLite database management for your projects. It provides a convenient wrapper around Asiosqlite, allowing easy definition of table and record schemas using Python\'s dataclasses. Define SQL tables and records effortlessly with AIODesa using a single data class, a tuple of data classes, or a .py file with dataclasses.\n\nAIODesa aims to make defining SQL tables and records easy by utilizing dataclasses to define schemas of tables and records. Table and record schemas can be defined with a single data class, a tuple of multiple data classes, or a .py file with dataclasses defined inside.\n\nFor example, define your table schemas in schemas.py\n\n![schema file](schemafile.png)\n\nImport db from the package and run with asyncio\n\nmain.py\n```\nfrom Database import Db\nimport asyncio\n\n\nasync def main():\n\tschema_file = "table_schemas.py"\n\tpath_to_generate_db = "database.sqlite3"\n\tasync with Db(path_to_generate_db) as db:\n\t\tawait db.read_table_schemas(schema_file)\n\nasyncio.run(main())\n```\n\nTables are automatically generated\n![sql file](sql.png)\n\n### Development:\nEnsure poetry is installed:\n```\npip install poetry\n```\n\nInstall project using poetry\n```\npoetry add git+https://github.com/sockheadrps/AIODesa.git\npoetry install\n```\n\ncreate a python file for using AIODesa and activate poetry virtual env to run it\n\n```\npoetry shell\npoetry run python main.py\n```\n\nSample API usage:\n```\nfrom dataclasses import dataclass\nfrom Database import Db\nimport asyncio\n\n\nasync def main():\n\t@dataclass\n\tclass Table:\n\t\tusername: str\n\t\tcredits: int\n\t\ttable_name: str = "table 1"\n\n\tschema = Table\n\t\n\tasync with Db("database.sqlite3") as db:\n\t\tawait db.read_table_schemas(schema)\n\nasyncio.run(main())\n```\n',
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

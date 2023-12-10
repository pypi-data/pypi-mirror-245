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
    'version': '0.1.5',
    'description': '',
    'long_description': '# Asyncio Dead Easy Sql API\n\n## AIODesa is for simple data access and definition for your python projects\n\n### AIODesa simplifies async SQLite database management for your projects. It provides a convenient wrapper around Asiosqlite, allowing easy definition of table and record schemas using Python\'s dataclasses. Define SQL tables and records effortlessly with AIODesa using a single data class, a tuple of data classes, or a .py file with dataclasses.\n\nAIODesa aims to make defining SQL tables and records easy by utilizing dataclasses to define schemas of tables and records. Table and record schemas can be defined with:\n1. a single data class\n2. a tuple of data classes\n3. a .py file with dataclasses.\n<br>\n\n# Usage\n\n__Install via pip__\n```\npip install aiodesa\n```\n\nFor example, define your table schemas in a seperate file.  \n__schemas.py__\n\n![schema file](https://github.com/sockheadrps/AIODesa/blob/main/schemafile.png?raw=true)\n\nImport db from the package and run with asyncio\n\n__main.py__\n\n```\nfrom aiodesa import Db\nimport asyncio\n\n\nasync def main():\n\tschema_file = "table_schemas.py"\n\tpath_to_generate_db = "database.sqlite3"\n\tasync with Db(path_to_generate_db) as db:\n\t\tawait db.read_table_schemas(schema_file)\n\nasyncio.run(main())\n```\n\nTables are automatically generated\n![sql file](https://github.com/sockheadrps/AIODesa/blob/main/sql.png?raw=true)\n\n<br>\n\n# Development:\n\nEnsure poetry is installed:\n\n```\npip install poetry\n```\n\nInstall project using poetry\n\n```\npoetry add git+https://github.com/sockheadrps/AIODesa.git\npoetry install\n```\n\ncreate a python file for using AIODesa and activate poetry virtual env to run it\n\n```\npoetry shell\npoetry run python main.py\n```\n\nSample API usage:\n\n```\nfrom dataclasses import dataclass\nfrom Database import Db\nimport asyncio\n\n\nasync def main():\n\t@dataclass\n\tclass Table:\n\t\tusername: str\n\t\tcredits: int\n\t\ttable_name: str = "table 1"\n\n\tschema = Table\n\n\tasync with Db("database.sqlite3") as db:\n\t\tawait db.read_table_schemas(schema)\n\nasyncio.run(main())\n```\n',
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
